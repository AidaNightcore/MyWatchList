from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus
from .models import User, UserRelationship
from api.middleware import jwt_required_middleware
from ..common.database import db

user_bp = Blueprint('user', __name__, url_prefix='/api/users')


@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required_middleware()
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict()), HTTPStatus.OK


@user_bp.route('/relationships', methods=['POST'])
@jwt_required_middleware()
def create_relationship():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    if not data or not data.get('related_user_id') or not data.get('type'):
        return jsonify({"error": "related_user_id and type are required"}), HTTPStatus.BAD_REQUEST

    relationship = UserRelationship(
        RelatingUserID=current_user_id,
        RelatedUserID=data['related_user_id'],
        Type=data['type']
    )
    db.session.add(relationship)
    db.session.commit()

    return jsonify({
        "id": relationship.id,
        "message": "Relationship created"
    }), HTTPStatus.CREATED