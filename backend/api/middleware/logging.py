from functools import wraps
from flask import request, jsonify, g, current_app
import time
import logging

def request_logging_middleware():
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            logger = logging.getLogger(__name__)

            try:
                # Log request
                logger.info(f"Incoming request: {request.method} {request.path}")

                response = fn(*args, **kwargs)
                duration = round((time.time() - start_time) * 1000, 2)

                # Log response
                status_code = response[1] if isinstance(response, tuple) else response.status_code
                logger.info(f"Request completed: {status_code} ({duration}ms)")

                return response

            except Exception as e:
                duration = round((time.time() - start_time) * 1000, 2)
                logger.error(f"Request failed: {str(e)} ({duration}ms)")
                raise

        return wrapper

    return decorator