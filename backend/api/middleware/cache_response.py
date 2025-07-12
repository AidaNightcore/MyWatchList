from functools import wraps
from flask import request, jsonify, current_app
from redis import Redis
import hashlib
import json

def cache_response(timeout=60):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            redis_url = current_app.config.get('REDIS_URL')
            if not redis_url:
                return fn(*args, **kwargs)
            client = Redis.from_url(redis_url)

            # Generează o cheie din endpoint și argumente query (hash pentru siguranță)
            raw_key = f"{request.endpoint}:{json.dumps(request.args, sort_keys=True)}"
            key = f"cache:{hashlib.md5(raw_key.encode()).hexdigest()}"

            cached = client.get(key)
            if cached:
                # Întoarce răspunsul direct din cache
                return jsonify(json.loads(cached))

            # Execută funcția, salvează în cache și returnează
            response = fn(*args, **kwargs)
            # Dacă răspunsul este un jsonify sau un tuple (răspuns, status), tratează corect
            if isinstance(response, tuple):
                data = response[0].get_json()
            else:
                data = response.get_json()
            client.setex(key, timeout, json.dumps(data))
            return response
        return wrapper
    return decorator
