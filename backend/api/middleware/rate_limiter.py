from functools import wraps
from flask import request, jsonify, g, current_app
from http import HTTPStatus
from redis import Redis

def rate_limit_middleware(requests=100, window=60):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Grab the URL from Flask’s config; bail out if unset
            redis_url = current_app.config.get('REDIS_URL')
            if not redis_url:
                return fn(*args, **kwargs)

            client = Redis.from_url(redis_url)

            key = f"rate_limit:{g.get('current_user_id','anon')}:{request.endpoint}"
            count = client.get(key)
            if count and int(count) >= requests:
                return jsonify({
                    "error": "Too many requests",
                    "limit": requests,
                    "window": window
                }), HTTPStatus.TOO_MANY_REQUESTS

            pipe = client.pipeline()
            pipe.incr(key, 1)
            pipe.expire(key, window)
            pipe.execute()

            return fn(*args, **kwargs)
        return wrapper
    return decorator
