from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus
from .models import Topic, Reply
from api.middleware import jwt_required_middleware
from ..common.database import db

social_bp = Blueprint('social', __name__, url_prefix='/api/social')


@social_bp.route('/topics', methods=['GET'])
def get_topics():
    topics = Topic.query.all()
    return jsonify([{
        'id': topic.id,
        'title': topic.title.title if topic.title else None,
        'reply_count': len(topic.replies)
    } for topic in topics]), HTTPStatus.OK


@social_bp.route('/topics', methods=['POST'])
@jwt_required_middleware()
def create_topic():
    data = request.get_json()
    if not data or not data.get('title_id'):
        return jsonify({"error": "title_id is required"}), HTTPStatus.BAD_REQUEST

    topic = Topic(titleID=data['title_id'])
    db.session.add(topic)
    db.session.commit()

    return jsonify({
        "id": topic.id,
        "message": "Topic created successfully"
    }), HTTPStatus.CREATED


@social_bp.route('/topics/<int:topic_id>/replies', methods=['POST'])
@jwt_required_middleware()
def create_reply(topic_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data or not data.get('message'):
        return jsonify({"error": "message is required"}), HTTPStatus.BAD_REQUEST

    reply = Reply(
        topicID=topic_id,
        userID=user_id,
        message=data['message']
    )
    db.session.add(reply)
    db.session.commit()

    return jsonify({
        "id": reply.id,
        "message": "Reply added successfully"
    }), HTTPStatus.CREATED