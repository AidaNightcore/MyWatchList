from datetime import datetime
from api.media.models import Title, TitleGenre, Genre, Type, Book, Movie, Show
from api.people.models import Crew, Job, Worker
from api.social.models import Topic
from api.common.database import db
import requests
from flask import current_app
from api.watchlist.models import WatchlistItem

def update_watch_status(entry, data):
    entry.status = data.get('status', entry.status)
    entry.score = data.get('score', entry.score)
    entry.favourite = data.get('favourite', entry.favourite)

    # Business logic example
    if entry.status == 'Completed' and not entry.endDate:
        entry.endDate = datetime.utcnow().date()


def create_title_with_metadata(title_str: str, type_name: str, genre_ids: list[int], crew_data: list[dict],
                               publisher_name=None) -> tuple[int, int]:
    # Ensure Type exists
    media_type = Type.query.filter_by(elementTypeName=type_name).first()
    if not media_type:
        media_type = Type(elementTypeName=type_name)
        db.session.add(media_type)
        db.session.flush()

    # Create Title
    title = Title(title=title_str, elementType=media_type.id)
    db.session.add(title)
    db.session.flush()  # flush to assign ID before committing

    # Link genres via TitleGenre
    for genre_id in genre_ids:
        db.session.add(TitleGenre(genreID=genre_id, titleID=title.id))

    if publisher_name:
        from api.media.models import Publisher
        pub_name = publisher_name.strip() or "Unknown"
        publisher = Publisher.query.filter_by(name=pub_name).first()
        if not publisher:
            publisher = Publisher(name=pub_name)
            db.session.add(publisher)
            db.session.flush()

    # Insert crew (acceptă și id, și nume)
    for entry in crew_data:
        worker_id = entry.get('worker_id')
        job_id = entry.get('job_id')
        worker = None
        job = None

        # Dacă avem id-uri
        if worker_id is not None and job_id is not None:
            worker = Worker.query.get(worker_id)
            if not worker:
                raise ValueError(f"Worker with id {worker_id} does not exist.")

            job = Job.query.get(job_id)
            if not job:
                raise ValueError(f"Job with id {job_id} does not exist.")

            if job.workerID != worker.id:
                raise ValueError(f"Job id {job_id} does not belong to worker id {worker_id}.")
        # Dacă avem nume
        elif entry.get('worker') and entry.get('job'):
            worker_name = entry['worker'].strip()
            job_title = entry['job'].strip()

            # Worker unic pe name
            worker = Worker.query.filter_by(name=worker_name).first()
            if worker is None:
                worker = Worker(name=worker_name)
                db.session.add(worker)
                db.session.flush()

            # Job unic pe title+workerID
            job = Job.query.filter_by(title=job_title, workerID=worker.id).first()
            if job is None:
                job = Job(title=job_title, workerID=worker.id)
                db.session.add(job)
                db.session.flush()
        else:
            raise ValueError("Each crew entry must have either (worker_id & job_id) or (worker & job)")

        # Crew (unic pe titleID, jobID)
        existing_crew = Crew.query.filter_by(titleID=title.id, jobID=job.id).first()
        if existing_crew is None:
            crew_row = Crew(titleID=title.id, jobID=job.id)
            db.session.add(crew_row)

    # Create Topic for this title
    topic = Topic(titleID=title.id)
    db.session.add(topic)

    db.session.commit()
    return title.id, media_type.id

def tastedive_recommend(title, type_="show", limit=10):
    api_key = current_app.config.get('TASTEDIVE_API_KEY')
    if not api_key:
        raise RuntimeError("TasteDive API key is missing in config.")
    url = "https://tastedive.com/api/similar"
    params = {
        "q": title,
        "type": type_,
        "k": api_key,
        "limit": limit,
        "info": 1
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()

def get_title_score(title):
    # ia toate WatchElement pentru acest title
    elements = WatchlistItem.query.filter_by(titleID=title.id).all()
    if elements:
        scores = [e.score for e in elements if e.score is not None]
        if scores:
            return sum(scores) / len(scores)
    return None

def get_publisher_name_for_title(title):
    if title.media_type and title.media_type.elementTypeName == "Book":
        book = Book.query.filter_by(typeID=title.id).first()
        if book and book.publisher:
            return book.publisher.name
    elif title.media_type and title.media_type.elementTypeName == "Movie":
        movie = Movie.query.filter_by(typeID=title.id).first()
        if movie and movie.publisher:
            return movie.publisher.name
    elif title.media_type and title.media_type.elementTypeName == "Show":
        show = Show.query.filter_by(typeID=title.id).first()
        if show and show.publisher:
            return show.publisher.name
    return None

