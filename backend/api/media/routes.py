from http import HTTPStatus
from flask import Blueprint, request, jsonify
from api.media.services import create_title_with_metadata
from api.middleware import jwt_required_middleware
from .models import (
    Book, Movie, Show, Season, Episode,
    Genre, Franchise, Publisher, Title, Type, TitleGenre
)
from ..common.database import db
from api.middleware.permissions import admin_required
import requests
from api.media.services import tastedive_recommend
from ..user.models import User
from ..watchlist.models import WatchlistItem, Watchlist

media_bp = Blueprint('media', __name__, url_prefix='/api/media')

@media_bp.route('/books', methods=['GET'])
@jwt_required_middleware()
def get_books():
    books = Book.query.all()

    return jsonify([{
        'id': book.id,
        'title': book.title,
        'genres': [genre.name for genre in book.genres],
        'publisher': book.publisher.name if book.publisher else None,
        'publish_date': book.publishDate.isoformat() if book.publishDate else None
    } for book in books]), HTTPStatus.OK

@media_bp.route('/movies', methods=['GET'])
@jwt_required_middleware()
def get_movies():
    movies = Movie.query.all()
    return jsonify([{
        'id': movie.id,
        'title': movie.title,
        'genre': movie.genre.name if movie.genre else None,
        'publish_date': movie.publishDate.isoformat() if movie.publishDate else None
    } for movie in movies]), HTTPStatus.OK

@media_bp.route('/shows', methods=['GET'])
@jwt_required_middleware()
def get_shows():
    shows = Show.query.all()
    return jsonify([{
        'id': show.id,
        'title': show.title,
        'seasons_count': len(show.seasons),
        'genres': [g.name for g in show.genres] if show.genres else []
    } for show in shows]), HTTPStatus.OK

@media_bp.route('/shows/<int:show_id>', methods=['GET'])
@jwt_required_middleware()
def get_show(show_id):
    show = Show.query.get_or_404(show_id)
    return jsonify({
        'id': show.id,
        'title': show.title,
        'franchise': show.franchise.title if show.franchise else None,
        'publisher': show.publisher.name if show.publisher else None,
        'seasons': [{
            'id': season.id,
            'season_number': season.seasonNumber,
            'publish_date': season.publishDate.isoformat() if season.publishDate else None,
            'episode_count': season.episodeCount
        } for season in show.seasons],
        'genres': [g.name for g in show.genres],
        'crew': show.crew
    }), HTTPStatus.OK


@media_bp.route('/shows/<int:show_id>/seasons', methods=['GET'])
@jwt_required_middleware()
def get_seasons(show_id):
    show = Show.query.get_or_404(show_id)
    return jsonify([{
        'id': season.id,
        'season_number': season.seasonNumber,
        'episode_count': season.episodeCount
    } for season in show.seasons]), HTTPStatus.OK

@media_bp.route('/seasons/<int:season_id>', methods=['GET'])
@jwt_required_middleware()
def get_season(season_id):
    season = Season.query.get_or_404(season_id)
    return jsonify({
        'id': season.id,
        'season_number': season.seasonNumber,
        'publish_date': season.publishDate.isoformat() if season.publishDate else None,
        'episode_count': season.episodeCount,
        'episodes': [{
            'id': ep.id,
            'title': ep.title,
            'publish_date': ep.publishDate.isoformat() if ep.publishDate else None
        } for ep in season.episodes]
    }), HTTPStatus.OK


@media_bp.route('/seasons/<int:season_id>/episodes', methods=['GET'])
@jwt_required_middleware()
def get_episodes(season_id):
    season = Season.query.get_or_404(season_id)
    return jsonify([{
        'id': ep.id,
        'title': ep.title,
        'publish_date': ep.publishDate.isoformat() if ep.publishDate else None,
        'synopsis': ep.synopsis,
        'genres': [g.name for g in ep.genres]
    } for ep in season.episodes]), HTTPStatus.OK

@media_bp.route('/episodes/<int:episode_id>', methods=['GET'])
@jwt_required_middleware()
def get_episode(episode_id):
    episode = Episode.query.get_or_404(episode_id)
    return jsonify({
        'id': episode.id,
        'title': episode.title,
        'publish_date': episode.publishDate.isoformat() if episode.publishDate else None,
        'synopsis': episode.synopsis,
        'season': {
            'id': episode.season.id,
            'season_number': episode.season.seasonNumber
        },
        'genres': [g.name for g in episode.genres],
        'crew': episode.crew
    }), HTTPStatus.OK

@media_bp.route('/books/<int:book_id>', methods=['GET'])
@jwt_required_middleware()
def get_book(book_id):
    book = Book.query.get_or_404(book_id)

    return jsonify({
        'id': book.id,
        'title': book.title,
        'genres': [g.name for g in book.genres],
        'publisher': book.publisher.name if book.publisher else None,
        'franchise': book.franchise.title if book.franchise else None,
        'publish_date': book.publishDate.isoformat() if book.publishDate else None,
        'crew': book.crew  # assumes you defined a @property crew
    }), HTTPStatus.OK

@media_bp.route('/movies/<int:movie_id>', methods=['GET'])
@jwt_required_middleware()
def get_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    return jsonify({
        'id': movie.id,
        'title': movie.title,
        'genres': [g.name for g in movie.genres],
        'publisher': movie.publisher.name if movie.publisher else None,
        'franchise': movie.franchise.title if movie.franchise else None,
        'publish_date': movie.publishDate.isoformat() if movie.publishDate else None,
        'crew': movie.crew
    }), HTTPStatus.OK

@media_bp.route('/search', methods=['GET'])
def search_media():
    query = request.args.get('q', '')
    if not query:
        return jsonify({"error": "Search query required"}), HTTPStatus.BAD_REQUEST

    # Search across all media types
    results = {
        'books': [b.to_dict() for b in Book.query.filter(Book.title.ilike(f'%{query}%')).all()],
        'movies': [m.to_dict() for m in Movie.query.filter(Movie.title.ilike(f'%{query}%')).all()],
        'shows': [s.to_dict() for s in Show.query.filter(Show.title.ilike(f'%{query}%')).all()]
    }

    return jsonify(results), HTTPStatus.OK

@media_bp.route('/book', methods=['POST'])
@jwt_required_middleware()
@admin_required
def create_book():
    data = request.get_json()

    # Resolve Publisher
    if 'publisher_id' not in data:
        if 'publisher_name' in data:
            publisher = Publisher.query.filter_by(name=data['publisher_name']).first()
            if not publisher:
                publisher = Publisher(name=data['publisher_name'])
                db.session.add(publisher)
                db.session.flush()
            publisher_id = publisher.id
        else:
            return jsonify({"error": "publisher_id or publisher_name required"}), HTTPStatus.BAD_REQUEST
    else:
        publisher_id = data['publisher_id']

    # Resolve Franchise
    franchise_id = None
    if 'franchise_id' in data:
        franchise_id = data['franchise_id']
    elif 'franchise_title' in data:
        franchise = Franchise.query.filter_by(title=data['franchise_title']).first()
        if not franchise:
            franchise = Franchise(title=data['franchise_title'])
            db.session.add(franchise)
            db.session.flush()
        franchise_id = franchise.id

    genre_ids = []
    if 'genre_names' in data:
        for name in data['genre_names']:
            genre = Genre.query.filter_by(name=name).first()
            if not genre:
                genre = Genre(name=name)
                db.session.add(genre)
                db.session.flush()
            genre_ids.append(genre.id)
    else:
        genre_ids = data.get('genre_ids', [])

    # Create Title and propagate genre & crew
    title_id, type_id = create_title_with_metadata(
        title_str=data['title'],
        type_name='Book',
        genre_ids=genre_ids,
        crew_data=data.get('crew', [])
    )

    # Create Book
    book = Book(
        title=data['title'],
        typeID=type_id,
        publisherID=publisher_id,
        franchiseID=franchise_id,
        goodreadsID=data.get('goodreads_id'),
        isbnID=data.get('isbn_id'),
        pages=data.get('pages'),
        ageRating=data.get('age_rating'),
        synopsis=data.get('synopsis'),
        publishDate=data.get('publish_date')
    )
    db.session.add(book)
    db.session.commit()

    return jsonify({"id": book.id, "message": "Book created"}), HTTPStatus.CREATED


@media_bp.route('/movie', methods=['POST'])
@jwt_required_middleware()
@admin_required
def create_movie():
    data = request.get_json()

    # Resolve Publisher
    if 'publisher_id' not in data:
        if 'publisher_name' in data:
            publisher = Publisher.query.filter_by(name=data['publisher_name']).first()
            if not publisher:
                publisher = Publisher(name=data['publisher_name'])
                db.session.add(publisher)
                db.session.flush()
            publisher_id = publisher.id
        else:
            return jsonify({"error": "publisher_id or publisher_name required"}), HTTPStatus.BAD_REQUEST
    else:
        publisher_id = data['publisher_id']

    # Resolve Franchise
    franchise_id = None
    if 'franchise_id' in data:
        franchise_id = data['franchise_id']
    elif 'franchise_title' in data:
        franchise = Franchise.query.filter_by(title=data['franchise_title']).first()
        if not franchise:
            franchise = Franchise(title=data['franchise_title'])
            db.session.add(franchise)
            db.session.flush()
        franchise_id = franchise.id

    genre_ids = []
    if 'genre_names' in data:
        for name in data['genre_names']:
            genre = Genre.query.filter_by(name=name).first()
            if not genre:
                genre = Genre(name=name)
                db.session.add(genre)
                db.session.flush()
            genre_ids.append(genre.id)
    else:
        genre_ids = data.get('genre_ids', [])

    title_id, type_id = create_title_with_metadata(
        title_str=data['title'],
        type_name='Movie',
        genre_ids=genre_ids,
        crew_data=data.get('crew', [])
    )

    movie = Movie(
        title=data['title'],
        typeID=type_id,
        franchiseID=franchise_id,
        publisherID=publisher_id,
        ageRating=data.get('age_rating'),
        synopsis=data.get('synopsis'),
        publishDate=data.get('publish_date'),
        imdbID=data.get('imdb_id')
    )
    db.session.add(movie)
    db.session.commit()

    return jsonify({"id": movie.id, "message": "Movie created"}), HTTPStatus.CREATED

@media_bp.route('/show', methods=['POST'])
@jwt_required_middleware()
@admin_required
def create_show():
    data = request.get_json()

    # Resolve Publisher
    if 'publisher_id' not in data:
        if 'publisher_name' in data:
            publisher = Publisher.query.filter_by(name=data['publisher_name']).first()
            if not publisher:
                publisher = Publisher(name=data['publisher_name'])
                db.session.add(publisher)
                db.session.flush()
            publisher_id = publisher.id
        else:
            return jsonify({"error": "publisher_id or publisher_name required"}), HTTPStatus.BAD_REQUEST
    else:
        publisher_id = data['publisher_id']

    # Resolve Franchise
    franchise_id = None
    if 'franchise_id' in data:
        franchise_id = data['franchise_id']
    elif 'franchise_title' in data:
        franchise = Franchise.query.filter_by(title=data['franchise_title']).first()
        if not franchise:
            franchise = Franchise(title=data['franchise_title'])
            db.session.add(franchise)
            db.session.flush()
        franchise_id = franchise.id

    genre_ids = []
    if 'genre_names' in data:
        for name in data['genre_names']:
            genre = Genre.query.filter_by(name=name).first()
            if not genre:
                genre = Genre(name=name)
                db.session.add(genre)
                db.session.flush()
            genre_ids.append(genre.id)
    else:
        genre_ids = data.get('genre_ids', [])

    title_id, type_id = create_title_with_metadata(
        title_str=data['title'],
        type_name='Show',
        genre_ids=genre_ids,
        crew_data=data.get('crew', [])
    )

    show = Show(
        title=data['title'],
        franchiseID=franchise_id,
        publisherID=publisher_id,
        ageRating=data.get('age_rating'),
        synopsis=data.get('synopsis'),
        imdbID=data.get('imdb_id')
    )
    db.session.add(show)
    db.session.commit()

    return jsonify({"id": show.id, "message": "Show created"}), HTTPStatus.CREATED

@media_bp.route('/shows/<int:show_id>/season', methods=['POST'])
@jwt_required_middleware()
@admin_required
def create_season(show_id):
    data = request.get_json()

    genre_ids = []
    if 'genre_names' in data:
        for name in data['genre_names']:
            genre = Genre.query.filter_by(name=name).first()
            if not genre:
                genre = Genre(name=name)
                db.session.add(genre)
                db.session.flush()
            genre_ids.append(genre.id)
    else:
        genre_ids = data.get('genre_ids', [])

    title_id, type_id = create_title_with_metadata(
        title_str=data['title'],
        type_name='Season',
        genre_ids=genre_ids,
        crew_data=data.get('crew', [])
    )

    season = Season(
        showID=show_id,
        seasonNumber=data['season_number'],
        synopsis=data.get('synopsis'),
        publishDate=data.get('publish_date'),
        episodeCount=data.get('episode_count')
    )
    db.session.add(season)
    db.session.commit()

    return jsonify({"id": season.id, "message": "Season created"}), HTTPStatus.CREATED

@media_bp.route('/seasons/<int:season_id>/episode', methods=['POST'])
@jwt_required_middleware()
@admin_required
def create_episode(season_id):
    data = request.get_json()

    genre_ids = []
    if 'genre_names' in data:
        for name in data['genre_names']:
            genre = Genre.query.filter_by(name=name).first()
            if not genre:
                genre = Genre(name=name)
                db.session.add(genre)
                db.session.flush()
            genre_ids.append(genre.id)
    else:
        genre_ids = data.get('genre_ids', [])

    title_id, type_id = create_title_with_metadata(
        title_str=data['title'],
        type_name='Episode',
        genre_ids=genre_ids,
        crew_data=data.get('crew', [])
    )

    episode = Episode(
        seasonID=season_id,
        title=data['title'],
        typeID=type_id,
        synopsis=data.get('synopsis'),
        publishDate=data.get('publish_date'),
        ageRating=data.get('age_rating')
    )
    db.session.add(episode)
    db.session.commit()

    return jsonify({"id": episode.id, "message": "Episode created"}), HTTPStatus.CREATED

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')
@admin_bp.route('/genres', methods=['POST'])
@jwt_required_middleware()
@admin_required
def create_genre():
    data = request.get_json()
    if not data.get('name'):
        return jsonify({"error": "Genre name is required"}), HTTPStatus.BAD_REQUEST

    genre = Genre(name=data['name'])
    db.session.add(genre)
    db.session.commit()
    return jsonify({"id": genre.id, "message": "Genre created"}), HTTPStatus.CREATED

@admin_bp.route('/franchises', methods=['POST'])
@jwt_required_middleware()
@admin_required
def create_franchise():
    data = request.get_json()
    if not data.get('title'):
        return jsonify({"error": "Franchise title is required"}), HTTPStatus.BAD_REQUEST

    franchise = Franchise(title=data['title'])
    db.session.add(franchise)
    db.session.commit()
    return jsonify({"id": franchise.id, "message": "Franchise created"}), HTTPStatus.CREATED

@admin_bp.route('/publishers', methods=['POST'])
@jwt_required_middleware()
@admin_required
def create_publisher():
    data = request.get_json()
    if not data.get('name'):
        return jsonify({"error": "Publisher name is required"}), HTTPStatus.BAD_REQUEST

    publisher = Publisher(name=data['name'])
    db.session.add(publisher)
    db.session.commit()
    return jsonify({"id": publisher.id, "message": "Publisher created"}), HTTPStatus.CREATED

@admin_bp.route('/lookup/genre', methods=['GET'])
def lookup_genre():
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "Genre name is required"}), HTTPStatus.BAD_REQUEST
    genre = Genre.query.filter_by(name=name).first()
    if not genre:
        return jsonify({"error": "Genre not found"}), HTTPStatus.NOT_FOUND
    return jsonify({"id": genre.id, "name": genre.name}), HTTPStatus.OK

@admin_bp.route('/lookup/franchise', methods=['GET'])
def lookup_franchise():
    title = request.args.get('title')
    if not title:
        return jsonify({"error": "Franchise title is required"}), HTTPStatus.BAD_REQUEST
    franchise = Franchise.query.filter_by(title=title).first()
    if not franchise:
        return jsonify({"error": "Franchise not found"}), HTTPStatus.NOT_FOUND
    return jsonify({"id": franchise.id, "title": franchise.title}), HTTPStatus.OK

@admin_bp.route('/lookup/publisher', methods=['GET'])
def lookup_publisher():
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "Publisher name is required"}), HTTPStatus.BAD_REQUEST
    publisher = Publisher.query.filter_by(name=name).first()
    if not publisher:
        return jsonify({"error": "Publisher not found"}), HTTPStatus.NOT_FOUND
    return jsonify({"id": publisher.id, "name": publisher.name}), HTTPStatus.OK

@admin_bp.route('/books/<int:book_id>', methods=['DELETE'])
@jwt_required_middleware()
@admin_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted'}), HTTPStatus.NO_CONTENT

@admin_bp.route('/movies/<int:movie_id>', methods=['DELETE'])
@jwt_required_middleware()
@admin_required
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return jsonify({'message': 'Movie deleted'}), HTTPStatus.NO_CONTENT

@admin_bp.route('/shows/<int:show_id>', methods=['DELETE'])
@jwt_required_middleware()
@admin_required
def delete_show(show_id):
    show = Show.query.get_or_404(show_id)
    db.session.delete(show)
    db.session.commit()
    return jsonify({'message': 'Show deleted'}), HTTPStatus.NO_CONTENT

@admin_bp.route('/seasons/<int:season_id>', methods=['DELETE'])
@jwt_required_middleware()
@admin_required
def delete_season(season_id):
    season = Season.query.get_or_404(season_id)
    db.session.delete(season)
    db.session.commit()
    return jsonify({'message': 'Season deleted'}), HTTPStatus.NO_CONTENT

@admin_bp.route('/episodes/<int:episode_id>', methods=['DELETE'])
@jwt_required_middleware()
@admin_required
def delete_episode(episode_id):
    episode = Episode.query.get_or_404(episode_id)
    db.session.delete(episode)
    db.session.commit()
    return jsonify({'message': 'Episode deleted'}), HTTPStatus.NO_CONTENT

@admin_bp.route('/genres/<int:genre_id>', methods=['DELETE'])
@jwt_required_middleware()
@admin_required
def delete_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    db.session.delete(genre)
    db.session.commit()
    return jsonify({'message': 'Genre deleted'}), HTTPStatus.NO_CONTENT

@admin_bp.route('/franchises/<int:franchise_id>', methods=['DELETE'])
@jwt_required_middleware()
@admin_required
def delete_franchise(franchise_id):
    franchise = Franchise.query.get_or_404(franchise_id)
    db.session.delete(franchise)
    db.session.commit()
    return jsonify({'message': 'Franchise deleted'}), HTTPStatus.NO_CONTENT

@admin_bp.route('/publishers/<int:publisher_id>', methods=['DELETE'])
@jwt_required_middleware()
@admin_required
def delete_publisher(publisher_id):
    publisher = Publisher.query.get_or_404(publisher_id)
    db.session.delete(publisher)
    db.session.commit()
    return jsonify({'message': 'Publisher deleted'}), HTTPStatus.NO_CONTENT

@admin_bp.route('/books/<int:book_id>', methods=['PUT'])
@jwt_required_middleware()
@admin_required
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.get_json()

    # Title și propagare în Title și Topic
    if 'title' in data:
        book.title = data['title']
        if book.typeID:
            title_obj = Title.query.get(book.typeID)
            if title_obj:
                title_obj.title = data['title']
                for topic in title_obj.topics:
                    topic.title = data['title']

    # Relații
    if 'publisher_id' in data:
        book.publisherID = data['publisher_id']
    if 'franchise_id' in data:
        book.franchiseID = data['franchise_id']

    # Atribute simple
    book.ageRating = data.get('ageRating', book.ageRating)
    book.synopsis = data.get('synopsis', book.synopsis)
    book.publishDate = data.get('publishDate', book.publishDate)
    book.isbnID = data.get('isbnID', book.isbnID)
    book.goodreadsID = data.get('goodreadsID', book.goodreadsID)
    book.pages = data.get('pages', book.pages)

    db.session.commit()
    return jsonify({'message': 'Book updated'}), HTTPStatus.OK


@admin_bp.route('/movies/<int:movie_id>', methods=['PUT'])
@jwt_required_middleware()
@admin_required
def update_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    data = request.get_json()

    if 'title' in data:
        movie.title = data['title']
        if movie.typeID:
            title_obj = Title.query.get(movie.typeID)
            if title_obj:
                title_obj.title = data['title']
                for topic in title_obj.topics:
                    topic.title = data['title']

    if 'publisher_id' in data:
        movie.publisherID = data['publisher_id']
    if 'franchise_id' in data:
        movie.franchiseID = data['franchise_id']

    movie.ageRating = data.get('ageRating', movie.ageRating)
    movie.synopsis = data.get('synopsis', movie.synopsis)
    movie.publishDate = data.get('publishDate', movie.publishDate)
    movie.imdbID = data.get('imdbID', movie.imdbID)

    db.session.commit()
    return jsonify({'message': 'Movie updated'}), HTTPStatus.OK


@admin_bp.route('/shows/<int:show_id>', methods=['PUT'])
@jwt_required_middleware()
@admin_required
def update_show(show_id):
    show = Show.query.get_or_404(show_id)
    data = request.get_json()

    if 'title' in data:
        show.title = data['title']
        if hasattr(show, 'typeID'):
            title_obj = Title.query.get(show.typeID)
            if title_obj:
                title_obj.title = data['title']
                for topic in title_obj.topics:
                    topic.title = data['title']

    if 'publisher_id' in data:
        show.publisherID = data['publisher_id']
    if 'franchise_id' in data:
        show.franchiseID = data['franchise_id']

    show.ageRating = data.get('ageRating', show.ageRating)
    show.synopsis = data.get('synopsis', show.synopsis)
    show.imdbID = data.get('imdbID', show.imdbID)

    db.session.commit()
    return jsonify({'message': 'Show updated'}), HTTPStatus.OK


@admin_bp.route('/seasons/<int:season_id>', methods=['PUT'])
@jwt_required_middleware()
@admin_required
def update_season(season_id):
    season = Season.query.get_or_404(season_id)
    data = request.get_json()

    if 'seasonNumber' in data:
        season.seasonNumber = data['seasonNumber']
    if 'synopsis' in data:
        season.synopsis = data['synopsis']
    if 'publishDate' in data:
        season.publishDate = data['publishDate']
    if 'episodeCount' in data:
        season.episodeCount = data['episodeCount']
    if 'show_id' in data:
        season.showID = data['show_id']

    db.session.commit()
    return jsonify({'message': 'Season updated'}), HTTPStatus.OK


@admin_bp.route('/episodes/<int:episode_id>', methods=['PUT'])
@jwt_required_middleware()
@admin_required
def update_episode(episode_id):
    episode = Episode.query.get_or_404(episode_id)
    data = request.get_json()

    if 'title' in data:
        episode.title = data['title']
        if episode.typeID:
            title_obj = Title.query.get(episode.typeID)
            if title_obj:
                title_obj.title = data['title']
                for topic in title_obj.topics:
                    topic.title = data['title']

    if 'season_id' in data:
        episode.seasonID = data['season_id']

    episode.ageRating = data.get('ageRating', episode.ageRating)
    episode.synopsis = data.get('synopsis', episode.synopsis)
    episode.publishDate = data.get('publishDate', episode.publishDate)

    db.session.commit()
    return jsonify({'message': 'Episode updated'}), HTTPStatus.OK


@admin_bp.route('/genres/<int:genre_id>', methods=['PUT'])
@jwt_required_middleware()
@admin_required
def update_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    data = request.get_json()
    if 'name' in data:
        genre.name = data['name']
    db.session.commit()
    return jsonify({'message': 'Genre updated'}), HTTPStatus.OK


@admin_bp.route('/publishers/<int:publisher_id>', methods=['PUT'])
@jwt_required_middleware()
@admin_required
def update_publisher(publisher_id):
    publisher = Publisher.query.get_or_404(publisher_id)
    data = request.get_json()
    if 'name' in data:
        publisher.name = data['name']
    db.session.commit()
    return jsonify({'message': 'Publisher updated'}), HTTPStatus.OK


@admin_bp.route('/franchises/<int:franchise_id>', methods=['PUT'])
@jwt_required_middleware()
@admin_required
def update_franchise(franchise_id):
    franchise = Franchise.query.get_or_404(franchise_id)
    data = request.get_json()
    if 'title' in data:
        franchise.title = data['title']
    if 'publisher' in data:
        franchise.publisher = data['publisher']
    if 'synopsis' in data:
        franchise.synopsis = data['synopsis']
    db.session.commit()
    return jsonify({'message': 'Franchise updated'}), HTTPStatus.OK

@media_bp.route('/genres', methods=['GET'])
@jwt_required_middleware()
def get_genres():
    genres = Genre.query.all()
    return jsonify([
        {'id': g.id, 'name': g.name}
        for g in genres
    ]), HTTPStatus.OK

@media_bp.route('/genres/<int:genre_id>', methods=['GET'])
@jwt_required_middleware()
def get_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    return jsonify({
        'id': genre.id,
        'name': genre.name,
        'titles': [t.title for t in genre.titles]
    }), HTTPStatus.OK

@media_bp.route('/franchises', methods=['GET'])
@jwt_required_middleware()
def get_franchises():
    franchises = Franchise.query.all()
    return jsonify([
        {
            'id': f.id,
            'title': f.title,
            'publisher': f.publisher,
            'synopsis': f.synopsis
        } for f in franchises
    ]), HTTPStatus.OK

@media_bp.route('/franchises/<int:franchise_id>', methods=['GET'])
@jwt_required_middleware()
def get_franchise(franchise_id):
    franchise = Franchise.query.get_or_404(franchise_id)
    return jsonify({
        'id': franchise.id,
        'title': franchise.title,
        'publisher': franchise.publisher,
        'synopsis': franchise.synopsis,
        'books': [b.title for b in franchise.books],
        'movies': [m.title for m in franchise.movies],
        'shows': [s.title for s in franchise.shows]
    }), HTTPStatus.OK

@media_bp.route('/publishers', methods=['GET'])
@jwt_required_middleware()
def get_publishers():
    publishers = Publisher.query.all()
    return jsonify([
        {'id': p.id, 'name': p.name}
        for p in publishers
    ]), HTTPStatus.OK

@media_bp.route('/publishers/<int:publisher_id>', methods=['GET'])
@jwt_required_middleware()
def get_publisher(publisher_id):
    publisher = Publisher.query.get_or_404(publisher_id)
    return jsonify({
        'id': publisher.id,
        'name': publisher.name,
        'books': [b.title for b in publisher.books],
        'movies': [m.title for m in publisher.movies],
        'shows': [s.title for s in publisher.shows]
    }), HTTPStatus.OK

@media_bp.route('/recommendations', methods=['GET'])
@jwt_required_middleware()
def get_recommendations():
    title = request.args.get('title')
    type_ = request.args.get('type', 'show')
    limit = int(request.args.get('limit', 10))
    if not title:
        return jsonify({"error": "Title required"}), 400
    try:
        data = tastedive_recommend(title, type_=type_, limit=limit)
    except requests.RequestException as e:
        return jsonify({"error": f"TasteDive API error: {str(e)}"}), 502
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(data)


@media_bp.route('/trending', methods=['GET'])
@jwt_required_middleware()
def get_media_trending():
    type_ = request.args.get('type')
    genre = request.args.get('genre')
    order_by = request.args.get('order_by', 'score')  # or 'publishDate'
    query = Title.query
    if type_:
        query = query.join(Type).filter(Type.elementTypeName == type_)
    if genre:
        query = query.join(TitleGenre).join(Genre).filter(Genre.name == genre)
    # Exemplu de trending: scor mediu descrescător, fallback la data publicării
    if order_by == 'score':
        query = query.order_by(Title.averageScore.desc())
    elif order_by == 'publishDate':
        query = query.order_by(Title.publishDate.desc())
    trending = query.limit(20).all()
    return jsonify([{
        'id': t.id,
        'title': t.title,
        'type': t.media_type.elementTypeName if t.media_type else None,
        'genres': t.genre_names,
        'averageScore': getattr(t, 'averageScore', None),
        'publishDate': getattr(t, 'publishDate', None)
    } for t in trending])

@media_bp.route('/search/advanced', methods=['GET'])
@jwt_required_middleware()
def media_advanced_search():
    type_ = request.args.get('type')
    genre = request.args.get('genre')
    year = request.args.get('year')
    min_score = request.args.get('min_score')
    q = request.args.get('q')

    query = Title.query
    if q:
        query = query.filter(Title.title.ilike(f"%{q}%"))
    if type_:
        query = query.join(Type).filter(Type.elementTypeName == type_)
    if genre:
        query = query.join(TitleGenre).join(Genre).filter(Genre.name == genre)
    if year:
        query = query.filter(db.extract('year', Title.publishDate) == int(year))
    if min_score and hasattr(Title, 'averageScore'):
        query = query.filter(Title.averageScore >= float(min_score))
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    items = query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        "items": [t.to_dict() for t in items.items],
        "total": items.total,
        "page": page,
        "per_page": per_page
    })

@media_bp.route('/recommendations/multi-type', methods=['GET'])
@jwt_required_middleware()
def multi_type_recommendations():
    title = request.args.get('title')
    types = request.args.get('type', 'show,movie,book')
    limit = int(request.args.get('limit', 10))
    if not title:
        return jsonify({"error": "Title required"}), 400
    try:
        data = tastedive_recommend(title, type_=types, limit=limit)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(data)

@media_bp.route('/<int:user_id>/dashboard/recommendations', methods=['GET'])
@jwt_required_middleware()
def dashboard_recommendations(user_id):
    user = User.query.get_or_404(user_id)
    # Get last 3-5 completed watchlist items
    last_items = (WatchlistItem.query
                  .join(Watchlist)
                  .filter(Watchlist.userID == user.id, WatchlistItem.status == 'completed')
                  .order_by(WatchlistItem.updated_at.desc())
                  .limit(5).all())
    recs = {}
    for item in last_items:
        title = item.title.title if item.title else None
        type_ = item.title.media_type.elementTypeName if item.title and item.title.media_type else 'show'
        if title:
            try:
                recs[title] = tastedive_recommend(title, type_=type_, limit=5)
            except Exception:
                recs[title] = {"error": "Could not fetch"}
    return jsonify(recs)

@media_bp.route('/<int:user_id>/watchlist/bulk-recommendations', methods=['GET'])
@jwt_required_middleware()
def bulk_watchlist_recommendations(user_id):
    user = User.query.get_or_404(user_id)
    items = WatchlistItem.query.join(Watchlist).filter(
        Watchlist.userID == user.id, WatchlistItem.status == 'completed'
    ).all()
    rec_map = {}
    for item in items:
        title = item.title.title if item.title else None
        type_ = item.title.media_type.elementTypeName if item.title and item.title.media_type else 'show'
        if title:
            try:
                rec_map[title] = tastedive_recommend(title, type_=type_, limit=2)
            except Exception:
                rec_map[title] = {"error": "Could not fetch"}
    return jsonify(rec_map)

@media_bp.route('/<int:user_id>/badges/recommendations', methods=['GET'])
@jwt_required_middleware()
def recommendation_badges(user_id):
    user = User.query.get_or_404(user_id)
    completed_titles = {item.title.title for item in WatchlistItem.query.join(Watchlist).filter(
        Watchlist.userID == user.id, WatchlistItem.status == 'completed'
    ).all() if item.title}
    badges = []
    # For each completed, check if user completed all top 3 recommendations for it
    for item in completed_titles:
        try:
            recs = tastedive_recommend(item, limit=3)
            rec_names = {r['Name'] for r in recs.get('Similar', {}).get('Results', [])}
            if rec_names and rec_names.issubset(completed_titles):
                badges.append({
                    "title": item,
                    "badge": f"Completed all recommendations for {item}"
                })
        except Exception:
            continue
    return jsonify(badges)

@media_bp.route('/<int:user_id>/recommendations/universe-expand', methods=['GET'])
@jwt_required_middleware()
def expand_my_universe(user_id):
    user = User.query.get_or_404(user_id)
    # Find user's most frequent genres from watchlist
    genre_counts = {}
    items = WatchlistItem.query.join(Watchlist).join(Title).join(TitleGenre).join(Genre).filter(
        Watchlist.userID == user.id
    ).all()
    for item in items:
        for genre in item.title.genres:
            genre_counts[genre.name] = genre_counts.get(genre.name, 0) + 1
    if not genre_counts:
        return jsonify({"error": "No genres found"}), 404
    top_genre = max(genre_counts, key=genre_counts.get)
    # Pick a random completed title from this genre
    from random import choice
    genre_titles = [item.title.title for item in items if top_genre in [g.name for g in item.title.genres]]
    if not genre_titles:
        return jsonify({"error": "No titles in top genre"}), 404
    chosen = choice(genre_titles)
    recs = tastedive_recommend(chosen, limit=5)
    return jsonify({
        "base_title": chosen,
        "top_genre": top_genre,
        "recommendations": recs.get('Similar', {}).get('Results', [])
    })

@media_bp.route('/<int:user_id>/recommendations/unlikely', methods=['GET'])
@jwt_required_middleware()
def unlikely_recommendations(user_id):
    user = User.query.get_or_404(user_id)
    completed_titles = {
        item.title.title
        for item in WatchlistItem.query.join(Watchlist).filter(
            Watchlist.userID == user.id,
            WatchlistItem.status == 'completed',
            WatchlistItem.titleID.isnot(None)
        ).all()
        if item.title
    }
    not_liked = []
    if not completed_titles:
        return jsonify({"error": "No completed items"}), 404
    title = list(completed_titles)[0]
    recs = tastedive_recommend(title, limit=10)
    all_recs = recs.get('Similar', {}).get('Results', [])
    for r in all_recs[::-1]:
        if r['Name'] not in completed_titles:
            not_liked.append(r)
        if len(not_liked) >= 5:
            break
    return jsonify(not_liked)

