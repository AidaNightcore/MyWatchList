from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus
from .models import Topic, Reply, Report
from api.middleware import jwt_required_middleware
from ..common.database import db
from ..media.models import Title
from ..middleware.permissions import admin_required, moderator_required
from ..user.models import User

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
@admin_required
@moderator_required
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

@social_bp.route('/replies/<int:reply_id>', methods=['DELETE'])
@jwt_required_middleware()
@admin_required
@moderator_required
def delete_reply(reply_id):
    reply = Reply.query.get_or_404(reply_id)
    db.session.delete(reply)
    db.session.commit()
    return jsonify({"message": "Reply deleted"}), HTTPStatus.NO_CONTENT

@social_bp.route('/replies/<int:reply_id>', methods=['PUT'])
@jwt_required_middleware()
def update_reply(reply_id):
    from flask_jwt_extended import get_jwt_identity
    from api.user.models import User
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    reply = Reply.query.get_or_404(reply_id)

    # Permisiuni: admin, moderator sau autor reply
    if not user or (not user.isAdmin and not user.isModerator and user.id != reply.userID):
        return jsonify({"error": "Permission denied"}), HTTPStatus.FORBIDDEN

    data = request.get_json()
    if "message" in data:
        reply.message = data["message"]
    db.session.commit()
    return jsonify({"message": "Reply updated"}), HTTPStatus.OK

@social_bp.route('/reports', methods=['GET'])
@jwt_required_middleware()
@admin_required
@moderator_required
def get_reports():
    reports = Report.query.all()
    return jsonify([
        {
            "id": r.id,
            "reporter_id": r.reporterID,
            "reported_user_id": r.reportedUserID,
            "reply_id": r.replyID,
            "created_at": r.createdAt.isoformat() if r.createdAt else None
        }
        for r in reports
    ]), HTTPStatus.OK

@social_bp.route('/reports/<int:report_id>', methods=['GET'])
@jwt_required_middleware()
@admin_required
@moderator_required
def get_report(report_id):
    report = Report.query.get_or_404(report_id)
    return jsonify({
        "id": report.id,
        "reporter_id": report.reporterID,
        "reported_user_id": report.reportedUserID,
        "reply_id": report.replyID,
        "created_at": report.createdAt.isoformat() if report.createdAt else None
    }), HTTPStatus.OK

@social_bp.route('/reports', methods=['POST'])
@jwt_required_middleware()
def create_report():
    user_id = get_jwt_identity()
    data = request.get_json()
    report = Report(
        reporterID=user_id,
        reportedUserID=data.get("reported_user_id"),
        replyID=data.get("reply_id")
    )
    db.session.add(report)
    db.session.commit()
    return jsonify({"id": report.id, "message": "Report created"}), HTTPStatus.CREATED

@social_bp.route('/reports/<int:report_id>', methods=['PUT'])
@jwt_required_middleware()
@admin_required
@moderator_required
def update_report(report_id):
    report = Report.query.get_or_404(report_id)
    data = request.get_json()
    if "reported_user_id" in data:
        report.reportedUserID = data["reported_user_id"]
    if "reply_id" in data:
        report.replyID = data["reply_id"]
    db.session.commit()
    return jsonify({"message": "Report updated"}), HTTPStatus.OK

@social_bp.route('/topics/search', methods=['GET'])
def forum_topic_search():
    q = request.args.get("q", "")
    if not q:
        return jsonify([]), 200
    topics = Topic.query.join(Title).filter(
        (Title.title.ilike(f"%{q}%"))
    ).all()
    return jsonify([
        {
            'id': t.id,
            'title': t.title.title if t.title else None,
            'reply_count': len(t.replies)
        }
        for t in topics
    ])
