from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus
from .models import Watchlist, WatchlistItem
from api.middleware import jwt_required_middleware
from api import db
watchlist_bp = Blueprint('watchlist', __name__, url_prefix='/api/watchlists')


@watchlist_bp.route('', methods=['GET'])
@jwt_required_middleware()
def get_watchlist():
    user_id = get_jwt_identity()
    watchlist = Watchlist.query.filter_by(user_id=user_id).first()

    if not watchlist:
        return jsonify({"message": "No watchlist found"}), HTTPStatus.OK

    return jsonify({
        "id": watchlist.id,
        "items": [item.to_dict() for item in watchlist.items]
    }), HTTPStatus.OK


@watchlist_bp.route('/items', methods=['POST'])
@jwt_required_middleware()
def add_to_watchlist():
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data or not data.get('title_id'):
        return jsonify({"error": "title_id is required"}), HTTPStatus.BAD_REQUEST

    # Get or create watchlist
    watchlist = Watchlist.query.filter_by(user_id=user_id).first()
    if not watchlist:
        watchlist = Watchlist(user_id=user_id)
        db.session.add(watchlist)
        db.session.commit()

    # Create new item
    item = WatchlistItem(
        watchlist_id=watchlist.id,
        title_id=data['title_id'],
        status=data.get('status', 'planned'),
        score=data.get('score'),
        progress=data.get('progress', 0)
    )

    if errors := item.validate():
        return jsonify({"errors": errors}), HTTPStatus.BAD_REQUEST

    db.session.add(item)
    db.session.commit()

    return jsonify(item.to_dict()), HTTPStatus.CREATED


@watchlist_bp.route('/items/<int:item_id>', methods=['PUT'])
@jwt_required_middleware()
def update_watchlist_item(item_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    item = WatchlistItem.query.join(Watchlist) \
        .filter(
        WatchlistItem.id == item_id,
        Watchlist.user_id == user_id
    ).first_or_404()

    if 'status' in data:
        item.status = data['status']
    if 'score' in data:
        item.score = data['score']
    if 'progress' in data:
        item.progress = data['progress']

    if errors := item.validate():
        return jsonify({"errors": errors}), HTTPStatus.BAD_REQUEST

    db.session.commit()
    return jsonify(item.to_dict()), HTTPStatus.OK