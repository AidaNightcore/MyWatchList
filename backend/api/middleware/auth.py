from functools import wraps
from flask import request, jsonify, g
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from http import HTTPStatus

PUBLIC_ENDPOINTS = {
    'user.get_user',
    'social.get_topics',
    'social.get_replies',
    'people.get_crew_for_title',
    'people.get_workers',
    'media.get_books',
    'media.get_movies',
    'media.get_shows',
    'media.get_seasons',
    'media.get_episodes',
    'media.search_media',
    'media.get_show',
    'media.get_season',
    'media.get_episode',
    'media.get_book',
    'media.lookup_genre',
    'media.lookup_franchise',
    'media.lookup_publisher',
    'media.get_movie',
    'media.get_publishers',
    'media.get_publishers',
    'media.get_franchises',
    'media.get_franchise',
    'media.get_genre',
    'media.get_genres',
    'media.get_all_titles'

}

def jwt_required_middleware():
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if request.method == 'GET' and request.endpoint in PUBLIC_ENDPOINTS:
                return fn(*args, **kwargs)

            try:
                verify_jwt_in_request()
                jwt_data = get_jwt()
                g.current_user_id = jwt_data['sub']

                # if not jwt_data.get('is_active', True):
                #     return jsonify({"error": "Account inactive"}), HTTPStatus.FORBIDDEN

            except Exception as e:
                return jsonify({
                    "error": "Invalid or missing token",
                    "details": str(e)
                }), HTTPStatus.UNAUTHORIZED

            return fn(*args, **kwargs)

        return wrapper

    return decorator
