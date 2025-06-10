from functools import wraps
from flask import request, jsonify, g, current_app


def cors_middleware():
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if request.method == 'OPTIONS':
                response = jsonify()
            else:
                response = fn(*args, **kwargs)

            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
            return response

        return wrapper

    return decorator