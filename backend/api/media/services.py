from datetime import datetime
from api.media.models import Title, TitleGenre, Genre, Type
from api.people.models import Crew, Job, Worker
from api.social.models import Topic
from api.common.database import db
import requests
from flask import current_app

def update_watch_status(entry, data):
    entry.status = data.get('status', entry.status)
    entry.score = data.get('score', entry.score)
    entry.favourite = data.get('favourite', entry.favourite)

    # Business logic example
    if entry.status == 'Completed' and not entry.endDate:
        entry.endDate = datetime.utcnow().date()


def create_title_with_metadata(title_str: str, type_name: str, genre_ids: list[int], crew_data: list[dict]) -> tuple[int, int]:
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

    # Insert crew
    for entry in crew_data:
        job_title = entry['job_title']
        worker_name = entry['worker_name']

        # Ensure Worker exists
        worker = Worker.query.filter_by(name=worker_name).first()
        if not worker:
            worker = Worker(name=worker_name)
            db.session.add(worker)
            db.session.flush()

        # Ensure Job exists and is uniquely tied to that worker
        job = Job.query.filter_by(title=job_title, workerID=worker.id).first()
        if not job:
            job = Job(title=job_title, workerID=worker.id)
            db.session.add(job)
            db.session.flush()

        # Check if Crew already exists
        existing_crew = Crew.query.filter_by(titleID=title.id, jobID=job.id).first()
        if not existing_crew:
            db.session.add(Crew(titleID=title.id, jobID=job.id))

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