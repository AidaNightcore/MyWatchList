from flask import jsonify
from http import HTTPStatus

def handle_not_found(e):
    return jsonify({"error": "Resource not found"}), HTTPStatus.NOT_FOUND

def handle_bad_request(e):
    return jsonify({"error": "Bad request"}), HTTPStatus.BAD_REQUEST

def handle_unauthorized(e):
    return jsonify({"error": "Unauthorized"}), HTTPStatus.UNAUTHORIZED

def register_error_handlers(app):
    app.register_error_handler(404, handle_not_found)
    app.register_error_handler(400, handle_bad_request)
    app.register_error_handler(401, handle_unauthorized)