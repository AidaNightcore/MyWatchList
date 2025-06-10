from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from http import HTTPStatus
from api.user.models import User
from api.common.database import db

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = db.session.get(User, user_id)

        if not user or not user.isAdmin:
            return jsonify({"error": "Admin access required"}), HTTPStatus.FORBIDDEN

        return fn(*args, **kwargs)
    return wrapper

def moderator_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = db.session.get(User, user_id)

        if not user or not user.isModerator:
            return jsonify({"error": "Moderator access required"}), HTTPStatus.FORBIDDEN

        return fn(*args, **kwargs)
    return wrapper