from flask import Blueprint, request, jsonify
from .models import Watchlist, WatchElement
from api.auth.models import User
from api.common.database import db
from .services import update_watch_status

watchlist_bp = Blueprint('watchlist', __name__, url_prefix='/watchlists')


@watchlist_bp.route('/<int:user_id>/entries', methods=['POST'])
def add_to_watchlist(user_id):
    data = request.json
    user = User.query.get_or_404(user_id)

    # Get or create watchlist
    watchlist = Watchlist.query.filter_by(userID=user_id).first()
    if not watchlist:
        watchlist = Watchlist(userID=user_id)
        db.session.add(watchlist)

    new_entry = WatchElement(
        titleID=data['title_id'],
        watchlistID=watchlist.id,
        status=data['status']
    )
    db.session.add(new_entry)
    db.session.commit()

    return jsonify(new_entry.serialize()), 201


@watchlist_bp.route('/entries/<int:entry_id>', methods=['PUT'])
def update_entry(entry_id):
    data = request.json
    entry = WatchElement.query.get_or_404(entry_id)
    update_watch_status(entry, data)  # Business logic in services
    db.session.commit()
    return jsonify(entry.serialize())