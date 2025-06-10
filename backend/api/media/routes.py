from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from http import HTTPStatus
from .models import (
    Book, Movie, Show, Season, Episode,
    Title, Genre, Franchise, Publisher, Type
)
from api.middleware import jwt_required_middleware, rate_limit_middleware

media_bp = Blueprint('media', __name__, url_prefix='/api/media')

@media_bp.route('/books', methods=['GET'])
@jwt_required_middleware()
@rate_limit_middleware(requests=100, window=60)
def get_books():
    books = Book.query.all()
    return jsonify([{
        'id': book.id,
        'title': book.title,
        'genre': book.genre.name if book.genre else None,
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
        'genre': show.genre.name if show.genre else None
    } for show in shows]), HTTPStatus.OK

@media_bp.route('/shows/<int:show_id>/seasons', methods=['GET'])
@jwt_required_middleware()
def get_seasons(show_id):
    show = Show.query.get_or_404(show_id)
    return jsonify([{
        'id': season.id,
        'season_number': season.seasonNumber,
        'episode_count': season.episodeCount
    } for season in show.seasons]), HTTPStatus.OK

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