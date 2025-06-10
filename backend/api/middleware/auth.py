from functools import wraps
from flask import request, jsonify, g
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from http import HTTPStatus


def jwt_required_middleware():
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                jwt_data = get_jwt()
                g.current_user_id = jwt_data['sub']

                if not jwt_data.get('is_active', True):
                    return jsonify({"error": "Account inactive"}), HTTPStatus.FORBIDDEN

            except Exception as e:
                return jsonify({
                    "error": "Invalid or missing token",
                    "details": str(e)
                }), HTTPStatus.UNAUTHORIZED

            return fn(*args, **kwargs)

        return wrapper

    return decorator