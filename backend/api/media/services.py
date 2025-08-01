from datetime import datetime
from api.media.models import Title, TitleGenre, Genre, Type, Book, Movie, Show, Publisher
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


def create_media_with_metadata(data, element_type):
    # 1. Publisher
    publisher_id = None
    publisher_name = data.get('publisher_name')
    if publisher_name:
        publisher = Publisher.query.filter_by(name=publisher_name.strip()).first()
        if not publisher:
            publisher = Publisher(name=publisher_name.strip())
            db.session.add(publisher)
            db.session.flush()
        publisher_id = publisher.id

    # 2. Select model și câmpuri specifice
    model_cls = {"Book": Book, "Movie": Movie}[element_type]
    model_kwargs = {
        "title": data['title'],
        "publisherID": publisher_id,
        "synopsis": data.get('synopsis'),
        "publishDate": data.get('publishDate'),  # trebuie camelCase și numele din model!
        "imgURL": data.get('imgURL')  # la fel!
    }
    if element_type == "Book":
        model_kwargs["isbnID"] = data.get('isbnID')
        model_kwargs["pages"] = data.get('pages')
    elif element_type == "Movie":
        model_kwargs["duration"] = data.get('duration')
        model_kwargs["publishDate"] = data.get('publishDate')

    # 3. Creează media_obj (fără typeID)
    media_obj = model_cls(**model_kwargs)
    db.session.add(media_obj)
    db.session.flush()  # media_obj.id disponibil

    # 4. Creează Type (id = media_obj.id)
    media_type = Type(id=media_obj.id, elementTypeName=element_type)
    db.session.add(media_type)
    db.session.flush()  # media_type.typeID disponibil

    # 5. Creează Title, cu titlul preluat din media_obj și elementType = typeID
    title_entry = Title(title=media_obj.title, elementType=media_type.typeID)
    db.session.add(title_entry)
    db.session.flush()  # title_entry.id disponibil

    # 6. Updatează media_obj cu typeID și titleID (dacă modelul are titleID ca FK)
    media_obj.typeID = media_type.typeID
    if hasattr(media_obj, "titleID"):
        media_obj.titleID = title_entry.id
    db.session.flush()

    # 7. Genuri (legate la Title)
    genre_names = data.get('genre_names', [])
    for genre_name in genre_names:
        genre_name = genre_name.strip()
        if not genre_name:
            continue
        genre = Genre.query.filter_by(name=genre_name).first()
        if not genre:
            genre = Genre(name=genre_name)
            db.session.add(genre)
            db.session.flush()
        # Asociază doar dacă nu există deja asocierea
        if not TitleGenre.query.filter_by(genreID=genre.id, titleID=title_entry.id).first():
            db.session.add(TitleGenre(genreID=genre.id, titleID=title_entry.id))

    # 8. Crew (legate la Title)
    crew_data = data.get('crew', [])
    for entry in crew_data:
        worker_name = entry.get('worker')
        job_title = entry.get('job')
        if not worker_name or not job_title:
            continue
        worker = Worker.query.filter_by(name=worker_name.strip()).first()
        if not worker:
            worker = Worker(name=worker_name.strip())
            db.session.add(worker)
            db.session.flush()
        job = Job.query.filter_by(title=job_title.strip(), workerID=worker.id).first()
        if not job:
            job = Job(title=job_title.strip(), workerID=worker.id)
            db.session.add(job)
            db.session.flush()
        existing_crew = Crew.query.filter_by(titleID=title_entry.id, jobID=job.id).first()
        if not existing_crew:
            db.session.add(Crew(titleID=title_entry.id, jobID=job.id))

    # 9. Topic (opțional, pentru forum/discuții, pe Title)
    topic = Topic(titleID=title_entry.id)
    db.session.add(topic)

    db.session.commit()
    return {
        "media_id": media_obj.id,
        "typeID": media_type.typeID,
        "titleID": title_entry.id
    }

from api.media.models import Show, Season, Episode, Genre, Title, TitleGenre, Publisher, Type
from api.people.models import Worker, Job, Crew
from api.social.models import Topic
from api.common.database import db

def create_episode_with_metadata(data):

    # 1. Show
    show_title = data['show_title'].strip()
    show = Show.query.filter_by(title=show_title).first()
    if not show:
        show = Show(title=show_title)
        db.session.add(show)
        db.session.flush()

    # 2. Season
    season_number = data['season_number']
    season = Season.query.filter_by(number=season_number, showID=show.id).first()
    if not season:
        season = Season(number=season_number, showID=show.id)
        db.session.add(season)
        db.session.flush()

    # 3. Episode (fără typeID, fără titleID inițial)
    episode_title = data['episode_title'].strip()
    episode = Episode(
        title=episode_title,
        number=data['episode_number'],
        seasonID=season.id,
        synopsis=data.get('synopsis'),
        publish_date=data.get('publish_date'),
        image_url=data.get('image_url')
    )
    db.session.add(episode)
    db.session.flush()  # episode.id devine disponibil

    # 4. Type (doar pentru episod)
    media_type = Type(id=episode.id, elementTypeName='Episode')
    db.session.add(media_type)
    db.session.flush()  # media_type.typeID devine disponibil

    # 5. Title (pentru episod, legat la Type)
    title_entry = Title(title=episode_title, elementType=media_type.typeID)
    db.session.add(title_entry)
    db.session.flush()  # title_entry.id devine disponibil

    # 6. Update episode cu typeID și titleID
    episode.typeID = media_type.typeID
    if hasattr(episode, "titleID"):
        episode.titleID = title_entry.id
    db.session.flush()

    # 7. Genuri (legate la title_entry)
    genre_names = data.get('genre_names', [])
    for genre_name in genre_names:
        genre = Genre.query.filter_by(name=genre_name).first()
        if not genre:
            genre = Genre(name=genre_name)
            db.session.add(genre)
            db.session.flush()
        db.session.add(TitleGenre(genreID=genre.id, titleID=title_entry.id))

    # 8. Crew (legate la title_entry)
    crew_data = data.get('crew', [])
    for entry in crew_data:
        worker_name = entry.get('worker')
        job_title = entry.get('job')
        if not worker_name or not job_title:
            continue
        worker = Worker.query.filter_by(name=worker_name.strip()).first()
        if not worker:
            worker = Worker(name=worker_name.strip())
            db.session.add(worker)
            db.session.flush()
        job = Job.query.filter_by(title=job_title.strip(), workerID=worker.id).first()
        if not job:
            job = Job(title=job_title.strip(), workerID=worker.id)
            db.session.add(job)
            db.session.flush()
        existing_crew = Crew.query.filter_by(titleID=title_entry.id, jobID=job.id).first()
        if not existing_crew:
            db.session.add(Crew(titleID=title_entry.id, jobID=job.id))

    # 9. Topic
    topic = Topic(titleID=title_entry.id)
    db.session.add(topic)

    db.session.commit()
    return {
        "show_id": show.id,
        "season_id": season.id,
        "episode_id": episode.id,
        "typeID": media_type.typeID,
        "titleID": title_entry.id
    }



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

def get_element_details_for_title(title):
    if not title or not title.media_type:
        return None
    type_name = title.media_type.elementTypeName
    if type_name == "Book":
        obj = Book.query.filter_by(title=title.title, typeID=title.elementType).first()
    elif type_name == "Movie":
        obj = Movie.query.filter_by(title=title.title, typeID=title.elementType).first()
    elif type_name == "Episode":
        obj = Episode.query.filter_by(title=title.title, typeID=title.elementType).first()
    elif type_name == "Show":
        obj = Show.query.filter_by(title=title.title).first()
    elif type_name == "Season":
        obj = Season.query.filter_by(title=title.title).first()
    else:
        obj = None
    return obj.to_dict() if obj else None
