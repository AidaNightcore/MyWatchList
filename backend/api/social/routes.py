from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus

from sqlalchemy.orm import joinedload

from .models import Topic, Reply, Report
from api.middleware import jwt_required_middleware
from ..common.database import db
from ..media.models import Title, Book, Movie, Show, Type
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
def delete_reply(reply_id):
    user_id = get_jwt_identity()
    reply = Reply.query.get_or_404(reply_id)
    user = User.query.get(user_id)

    if not user or (not user.isAdmin and not user.isModerator and user.id != reply.userID):
        return jsonify({"error": "Permission denied"}), HTTPStatus.FORBIDDEN

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
@social_bp.route('/topics/board', methods=['GET'])
def get_topics_board():
    # Citește toate tipurile ca să ai maparea typeID → denumire
    type_id_to_name = {t.typeID: t.elementTypeName for t in Type.query.all()}
    result = {t: [] for t in ["Book", "Movie", "Show"]}

    # Extrage toate topicurile cu titlu asociat
    topics = (
        db.session.query(Topic)
        .options(joinedload(Topic.title))
        .order_by(Topic.id.desc())
        .all()
    )

    # Grupare pe tip după Titles.elementType
    grouped = {t: [] for t in ["Book", "Movie", "Show"]}
    for topic in topics:
        title = topic.title
        if not title:
            continue
        tip = type_id_to_name.get(title.elementType)
        if tip in grouped:
            grouped[tip].append(topic)

    for tip in ["Book", "Movie", "Show"]:
        for topic in grouped[tip][:5]:
            title = topic.title

            entry = None
            if tip == "Book":
                entry = Book.query.filter_by(title=title.title, typeID=title.elementType).first()
            elif tip == "Movie":
                entry = Movie.query.filter_by(title=title.title, typeID=title.elementType).first()
            elif tip == "Show":
                # Show nu are typeID în model, deci asociezi doar după title
                entry = Show.query.filter_by(title=title.title).first()
            if not entry:
                continue

            # Primul reply (cel mai vechi)
            first_reply = (
                Reply.query.filter_by(topicID=topic.id)
                .order_by(Reply.id.asc())
                .first()
            )
            result[tip].append({
                "id": topic.id,
                "mediaId": title.id,  # <-- Adaugă această linie!
                "title": title.title,
                "imgURL": getattr(entry, "imgURL", None),
                "question": getattr(entry, "synopsis", None),
                "firstReply": first_reply.message if first_reply else None,
            })

    return jsonify(result), 200

@social_bp.route('/topics/<int:topic_id>/replies', methods=['GET'])
def get_topic_with_replies(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    title = topic.title
    imgURL = None

    # Agregare imagine media
    if title:
        type_obj = Type.query.get(title.elementType)
        type_name = type_obj.elementTypeName if type_obj else None
        if type_name == "Book":
            book = Book.query.filter_by(title=title.title, typeID=title.elementType).first()
            if book and book.imgURL:
                imgURL = book.imgURL
        elif type_name == "Movie":
            movie = Movie.query.filter_by(title=title.title, typeID=title.elementType).first()
            if movie and movie.imgURL:
                imgURL = movie.imgURL
        elif type_name == "Show":
            show = Show.query.filter_by(title=title.title).first()
            if show and show.imgURL:
                imgURL = show.imgURL

    replies = (
        Reply.query.filter_by(topicID=topic_id)
        .order_by(Reply.id.asc())
        .all()
    )

    def reply_dict(reply):
        user = User.query.get(reply.userID) if hasattr(reply, 'userID') else None
        return {
            "id": reply.id,
            "userID": reply.userID,
            "user": {
                "id": user.id if user else None,
                "username": user.username if user else "Anonymous",
                "profilePicture": f"/api/users/{user.id}/profile-picture" if user and user.profilePicture else None,
                "createdAt": user.createdAt.isoformat() if user and user.createdAt else None,
                "lastLogin": user.lastLogin.isoformat() if user and user.lastLogin else None,
            },
            "message": reply.message,
            "createdAt": reply.date.isoformat() if reply.date else None,
        }

    return jsonify({
        "topic": {
            "id": topic.id,
            "title": title.title if title else "",
            "imgURL": imgURL,
            "mediaId": title.id if title else None,
            "firstReply": replies[0].message if replies else None
        },
        "replies": [reply_dict(r) for r in replies]
    }), 200

