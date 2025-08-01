from flask import Blueprint, request, jsonify, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus
from .models import User, UserRelationship
from api.middleware import jwt_required_middleware
from ..common.database import db
from api.middleware.permissions import admin_required, moderator_required
from ..media.models import Book, Movie, Show, Episode
from ..watchlist.models import Watchlist

user_bp = Blueprint('user', __name__, url_prefix='/api/users')

from api.common.email_service import (
    send_password_change_email,
    send_email_change_email,
    send_account_deletion_email
)

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

@user_bp.route('/<int:user_id>/relationships', methods=['GET'])
@jwt_required_middleware()
def get_user_relationships(user_id):
    user = User.query.get_or_404(user_id)
    all_rels = user.relationships_initiated + user.relationships_received
    grouped = {}
    for rel in all_rels:
        rel_type = rel.Type
        if rel_type not in grouped:
            grouped[rel_type] = []
        grouped[rel_type].append({
            "id": rel.id,
            "relating_user_id": rel.RelatingUserID,
            "related_user_id": rel.RelatedUserID
        })
    return jsonify(grouped), HTTPStatus.OK

@user_bp.route('/<int:user_id>/relationships/<string:type>', methods=['GET'])
@jwt_required_middleware()
def get_user_relationships_by_type(user_id, type):
    user = User.query.get_or_404(user_id)
    rels = UserRelationship.query.filter(
        ((UserRelationship.RelatingUserID == user.id) | (UserRelationship.RelatedUserID == user.id)) &
        (UserRelationship.Type == type)
    ).all()
    return jsonify([
        {
            "id": r.id,
            "relating_user_id": r.RelatingUserID,
            "related_user_id": r.RelatedUserID
        }
        for r in rels
    ]), HTTPStatus.OK

@user_bp.route('/<int:user_id>/profile-picture', methods=['GET'])
@jwt_required_middleware()
def get_profile_picture(user_id):
    user = User.query.get_or_404(user_id)
    if not user.profilePicture:
        return jsonify({"error": "No profile picture found"}), 404
    return Response(user.profilePicture, mimetype='image/jpeg')


@user_bp.route('/relationships/<int:relationship_id>', methods=['PUT'])
@jwt_required_middleware()
def update_relationship(relationship_id):
    rel = UserRelationship.query.get_or_404(relationship_id)
    current_user_id = get_jwt_identity()
    data = request.get_json()

    # Acceptare friend request: doar destinatarul poate accepta
    if rel.Type == "pending" and data.get("Type") == "friend":
        if rel.RelatedUserID != current_user_id:
            return jsonify({"error": "Not allowed"}), HTTPStatus.FORBIDDEN

        # Acceptă cererea (schimbă tipul și propagă relația inversă)
        rel.Type = "friend"
        inverse_rel = UserRelationship.query.filter_by(
            RelatingUserID=rel.RelatedUserID,
            RelatedUserID=rel.RelatingUserID
        ).first()
        if not inverse_rel:
            db.session.add(UserRelationship(
                RelatingUserID=rel.RelatedUserID,
                RelatedUserID=rel.RelatingUserID,
                Type="friend"
            ))
        db.session.commit()
        return jsonify({"message": "Friendship accepted"}), HTTPStatus.OK

    # Pentru alte modificări standard
    if "type" in data and data.get("Type") != rel.Type:
        rel.Type = data["type"]
    db.session.commit()
    return jsonify({"message": "Relationship updated"}), HTTPStatus.OK

@user_bp.route('/relationships/<int:user1_id>/<int:user2_id>/<string:type>', methods=['DELETE'])
@jwt_required_middleware()
def delete_relationship_by_type(user1_id, user2_id, type):
    current_user_id = int(get_jwt_identity())

    if current_user_id not in [user1_id, user2_id]:
        return jsonify({"error": "Not allowed"}), HTTPStatus.FORBIDDEN

    rels = UserRelationship.query.filter(
        (
            ((UserRelationship.RelatingUserID == user1_id) & (UserRelationship.RelatedUserID == user2_id)) |
            ((UserRelationship.RelatingUserID == user2_id) & (UserRelationship.RelatedUserID == user1_id))
        ) &
        (UserRelationship.Type == type)
    ).all()

    if not rels:
        return jsonify({"error": f"No {type} relationship found"}), HTTPStatus.NOT_FOUND

    for rel in rels:
        db.session.delete(rel)
    db.session.commit()
    return jsonify({"message": f"All '{type}' relationships between users deleted"}), HTTPStatus.NO_CONTENT

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required_middleware()
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    user_email = user.email
    send_account_deletion_email(user, email=user_email)
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted"}), HTTPStatus.NO_CONTENT

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required_middleware()
def delete_own_account(user_id):
    current_user_id = int(get_jwt_identity())
    if user_id != current_user_id:
        return jsonify({"error": "You can only delete your own account."}), HTTPStatus.FORBIDDEN

    user = User.query.get_or_404(user_id)
    user_email = user.email

    from api.common.email_service import send_account_deletion_email
    send_account_deletion_email(user, email=user_email)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Account deleted"}), HTTPStatus.NO_CONTENT

@user_bp.route('/<int:user_id>/mutuals/<int:other_user_id>', methods=['GET'])
@jwt_required_middleware()
def get_mutual_friends(user_id, other_user_id):
    user1 = User.query.get_or_404(user_id)
    user2 = User.query.get_or_404(other_user_id)
    u1_ids = {rel.RelatedUserID for rel in user1.relationships_initiated if rel.Type == "friend"}
    u1_ids.update({rel.RelatingUserID for rel in user1.relationships_received if rel.Type == "friend"})
    u2_ids = {rel.RelatedUserID for rel in user2.relationships_initiated if rel.Type == "friend"}
    u2_ids.update({rel.RelatingUserID for rel in user2.relationships_received if rel.Type == "friend"})
    mutual_ids = u1_ids & u2_ids
    mutuals = User.query.filter(User.id.in_(mutual_ids)).all()
    return jsonify([u.to_dict() for u in mutuals]), HTTPStatus.OK

@user_bp.route('/search', methods=['GET'])
@jwt_required_middleware()
def search_users():
    q = request.args.get("q", "")
    users = User.query.filter(User.username.ilike(f"%{q}%")).all()
    return jsonify([{"id": u.id, "username": u.username, "name": u.name} for u in users]), HTTPStatus.OK

@user_bp.route('/<int:user_id>/profile-picture', methods=['PUT'])
@jwt_required_middleware()
def update_profile_picture(user_id):
    user = User.query.get_or_404(user_id)
    current_user_id = int(get_jwt_identity())
    if current_user_id != user.id:
        return jsonify({"error": "No permission"}), HTTPStatus.FORBIDDEN

    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), HTTPStatus.BAD_REQUEST
    file = request.files['file']
    user.profilePicture = file.read()
    db.session.commit()
    return jsonify({"message": "Profile picture updated"}), HTTPStatus.OK



@user_bp.route('/<int:user_id>/role', methods=['PUT'])
@jwt_required_middleware()
@admin_required
@moderator_required
def update_user_role(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    if 'isAdmin' in data:
        user.isAdmin = bool(data['isAdmin'])
    if 'isModerator' in data:
        user.isModerator = bool(data['isModerator'])
    db.session.commit()
    return jsonify({"message": "Role updated"}), HTTPStatus.OK

@user_bp.route('/<int:user_id>/email', methods=['PUT'])
@jwt_required_middleware()
def update_user_email(user_id):
    user = User.query.get_or_404(user_id)
    current_user_id = int(get_jwt_identity())
    if current_user_id != user.id:
        return jsonify({"error": "No permission"}), HTTPStatus.FORBIDDEN

    data = request.get_json()
    if not data or 'email' not in data:
        return jsonify({"error": "Email required"}), HTTPStatus.BAD_REQUEST
    old_email = user.email
    user.email = data['email']
    db.session.commit()
    send_email_change_email(user, old_email, user.email)  # <-- send email here
    return jsonify({"message": "Email updated"}), HTTPStatus.OK

@user_bp.route('/<int:user_id>/password', methods=['PUT'])
@jwt_required_middleware()
def update_user_password(user_id):
    user = User.query.get_or_404(user_id)
    current_user_id = int(get_jwt_identity())
    if current_user_id != user.id:
        return jsonify({"error": "No permission"}), HTTPStatus.FORBIDDEN

    data = request.get_json()
    if not data or 'password' not in data:
        return jsonify({"error": "Password required"}), HTTPStatus.BAD_REQUEST
    user.set_password(data['password'])
    db.session.commit()
    send_password_change_email(user)
    return jsonify({"message": "Password updated"}), HTTPStatus.OK

@user_bp.route('/<int:user_id>/name', methods=['PUT'])
@jwt_required_middleware()
def update_user_name(user_id):
    user = User.query.get_or_404(user_id)
    current_user_id = int(get_jwt_identity())
    if current_user_id != user.id:
        return jsonify({"error": "No permission"}), HTTPStatus.FORBIDDEN

    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Name required"}), HTTPStatus.BAD_REQUEST
    user.name = data['name']
    db.session.commit()
    return jsonify({"message": "Name updated"}), HTTPStatus.OK


@user_bp.route('/<int:user_id>/username', methods=['PUT'])
@jwt_required_middleware()
def update_user_username(user_id):
    user = User.query.get_or_404(user_id)
    current_user_id = int(get_jwt_identity())
    if current_user_id != user.id:
        return jsonify({"error": "No permission"}), HTTPStatus.FORBIDDEN

    data = request.get_json()
    if not data or 'username' not in data:
        return jsonify({"error": "Username required"}), HTTPStatus.BAD_REQUEST
    user.username = data['username']
    db.session.commit()
    return jsonify({"message": "Username updated"}), HTTPStatus.OK


@user_bp.route('/profile-summary/<int:user_id>', methods=['GET'])
def profile_summary(user_id):
    user = User.query.get_or_404(user_id)
    watchlist = Watchlist.query.filter_by(userID=user_id).first()
    if not watchlist or not watchlist.items:
        return jsonify({
            "username": user.username,
            "id": user.id,
            "counts": {},
            "genre_distribution": {},
            "status_by_genre": {},
            "status_by_type": {},
            "pages_read": 0,
            "minutes_watched": 0
        }), 200

    counts = {}
    genre_distribution = {}
    status_by_genre = {}
    status_by_type = {}
    pages_read = 0
    minutes_watched = 0

    for item in watchlist.items:
        st = item.status
        counts[st] = counts.get(st, 0) + 1

        title = item.title
        details = getattr(item, "element_details", None) or {}

        genres = []
        pages = 0
        duration = 0

        if title and title.genres:
            genres = [g.name for g in title.genres]

        if details and hasattr(details, 'pages') and details.pages:
            pages = details.pages

        if details and hasattr(details,
                               'duration') and details.duration and title.media_type.elementTypeName == "Movie":
            if st == "completed":
                minutes_watched += details.duration

        if st == "completed" and title.media_type.elementTypeName == "Book":
            pages_read += pages

        if title and title.media_type.elementTypeName == "Show":
            progress = item.progress or 0
            all_episodes = []
            if hasattr(details, 'seasons'):
                for season in getattr(details, 'seasons', []):
                    all_episodes.extend(season.get('episodes', []))
            if all_episodes:
                episode_durations = [ep.get('duration', 0) for ep in all_episodes if ep.get('duration')]
                avg_ep_duration = sum(episode_durations) / len(episode_durations) if episode_durations else 0
                minutes_watched += progress * avg_ep_duration
            else:
                DEFAULT_EPISODE_MIN = 24
                minutes_watched += progress * DEFAULT_EPISODE_MIN
        if title and title.media_type.elementTypeName == "Episode":
            if details and hasattr(details, 'duration') and details.duration and st == "completed":
                minutes_watched += details.duration

        for g in genres:
            genre_distribution[g] = genre_distribution.get(g, 0) + 1
            if g not in status_by_genre:
                status_by_genre[g] = {}
            status_by_genre[g][st] = status_by_genre[g].get(st, 0) + 1

        # Agregare pe tip
        if title and title.media_type:
            type_name = title.media_type.elementTypeName
            if type_name not in status_by_type:
                status_by_type[type_name] = {}
            status_by_type[type_name][st] = status_by_type[type_name].get(st, 0) + 1

    return jsonify({
        "username": user.username,
        "id": user.id,
        "counts": counts,
        "genre_distribution": genre_distribution,
        "status_by_genre": status_by_genre,
        "status_by_type": status_by_type,
        "pages_read": pages_read,
        "minutes_watched": minutes_watched
    }), 200


@user_bp.route('/activity-history/<int:user_id>', methods=['GET'])
@jwt_required_middleware()
def activity_history(user_id):
    watchlist = Watchlist.query.filter_by(userID=user_id).first()
    if not watchlist or not watchlist.items:
        return jsonify([]), HTTPStatus.OK

    items = sorted(
        watchlist.items,
        key=lambda i: getattr(i, 'updated_at', None) or getattr(i, 'startDate', None) or getattr(i, 'endDate', None) or i.id,
        reverse=True
    )[:10]

    result = []
    for item in items:
        title = item.title
        if not title:
            continue

        type_name = title.media_type.elementTypeName if title.media_type else None
        image_url = None
        publish_date = None

        if type_name == "Book":
            book = Book.query.filter_by(title=title.title, typeID=title.elementType).first()
            if book:
                image_url = book.imgURL
                publish_date = book.publishDate.isoformat() if book.publishDate else None
        elif type_name == "Movie":
            movie = Movie.query.filter_by(title=title.title, typeID=title.elementType).first()
            if movie:
                image_url = movie.imgURL
                publish_date = movie.publishDate.isoformat() if movie.publishDate else None
        elif type_name == "Show":
            show = Show.query.filter_by(title=title.title).first()
            if show:
                image_url = show.imgURL
                # Shows don't have publishDate, can be ignored or set as None
        elif type_name == "Episode":
            episode = Episode.query.filter_by(title=title.title, typeID=title.elementType).first()
            if episode:
                image_url = episode.imgURL
                publish_date = episode.publishDate.isoformat() if episode.publishDate else None

        # Fallback la None dacă nu există
        if not image_url:
            image_url = None

        result.append({
            "id": title.id,
            "title": title.title,
            "type": type_name,
            "status": item.status,
            "date": str(getattr(item, 'startDate', None) or getattr(item, 'endDate', None) or ""),
            "score": item.score,
            "image_url": image_url,
            "publishDate": publish_date,
        })

    return jsonify(result), HTTPStatus.OK



