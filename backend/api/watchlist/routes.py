from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from http import HTTPStatus
from .models import Watchlist, WatchlistItem
from api.middleware import jwt_required_middleware
from api import db
from .services import enforce_progress
from ..media.models import Title, Type

from io import BytesIO

import pandas as pd
from flask import Response

from ..media.services import tastedive_recommend
from ..user.models import User

watchlist_bp = Blueprint('watchlist', __name__, url_prefix='/api/watchlists')

@watchlist_bp.route('', methods=['GET'])
@jwt_required_middleware()
def get_watchlists():
    user_id = int(get_jwt_identity())
    watchlist = Watchlist.query.filter_by(userID=user_id).first()
    if not watchlist:
        return jsonify({"message": "No watchlist found"}), HTTPStatus.OK

    grouped = {}
    for item in watchlist.items:
        grouped.setdefault(item.status, []).append(item.to_dict())
    return jsonify(grouped), HTTPStatus.OK

@watchlist_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_watchlist(user_id):
    watchlist = Watchlist.query.filter_by(userID=user_id).first()
    if not watchlist:
        return jsonify({"message": "No watchlist found"}), HTTPStatus.NOT_FOUND

    grouped = {}
    for item in watchlist.items:
        grouped.setdefault(item.status, []).append(item.to_dict())
    return jsonify(grouped), HTTPStatus.OK


@watchlist_bp.route('/<string:status>', methods=['GET'])
@jwt_required_middleware()
def get_watchlist_by_status(status):
    user_id = int(get_jwt_identity())
    valid_statuses = ['watching', 'completed', 'on_hold', 'dropped', 'planned']
    if status not in valid_statuses:
        return jsonify({"error": "Invalid status"}), HTTPStatus.BAD_REQUEST

    watchlist = Watchlist.query.filter_by(userID=user_id).first()
    if not watchlist:
        return jsonify({"message": "No watchlist found"}), HTTPStatus.OK

    items = [item.to_dict() for item in watchlist.items if item.status == status]
    return jsonify(items), HTTPStatus.OK


@watchlist_bp.route('/type/<string:type_name>', methods=['GET'])
@jwt_required_middleware()
def get_watchlist_by_type(type_name):
    user_id = int(get_jwt_identity())
    watchlist = Watchlist.query.filter_by(userID=user_id).first()
    if not watchlist:
        return jsonify({"message": "No watchlist found"}), HTTPStatus.OK

    filtered = [
        item.to_dict()
        for item in watchlist.items
        if item.title and item.title.media_type and item.title.media_type.elementTypeName.lower() == type_name.lower()
    ]
    return jsonify(filtered), HTTPStatus.OK


@watchlist_bp.route('/items/<int:item_id>', methods=['GET'])
@jwt_required_middleware()
def get_watchlist_item_by_id(item_id):
    user_id = int(get_jwt_identity())
    item = WatchlistItem.query.join(Watchlist).filter(
        WatchlistItem.id == item_id,
        Watchlist.userID == user_id
    ).first_or_404()
    return jsonify(item.to_dict()), HTTPStatus.OK

@watchlist_bp.route('/create', methods=['POST'])
@jwt_required_middleware()
def create_watchlist():
    userID = int(get_jwt_identity())
    existing = Watchlist.query.filter_by(userID=userID).first()
    if existing:
        return jsonify({"error": "Watchlist already exists"}), HTTPStatus.CONFLICT

    watchlist = Watchlist(userID=userID)
    db.session.add(watchlist)
    db.session.commit()
    return jsonify({"message": "Watchlist created", "id": watchlist.id}), HTTPStatus.CREATED

@watchlist_bp.route('/items', methods=['POST'])
@jwt_required_middleware()
def add_to_watchlist():
    userID = int(get_jwt_identity())

    data = request.get_json()
    if not data or not data.get('titleID'):
        return jsonify({"error": "titleID is required"}), HTTPStatus.BAD_REQUEST

    watchlist = Watchlist.query.filter_by(userID=userID).first()
    if not watchlist:
        watchlist = Watchlist(userID=userID)
        db.session.add(watchlist)
        db.session.commit()

    item = WatchlistItem.query.filter_by(watchlistID=watchlist.id, titleID=data['titleID']).first()
    created = False
    if item:
        # UPDATE logica
        item.status = data.get('status', item.status)
        item.score = data.get('score', item.score)
        item.progress = data.get('progress', item.progress)
        item.startDate = data.get('startDate', item.startDate)
        item.endDate = data.get('endDate', item.endDate)
        item.favourite = data.get('favourite', item.favourite)
    else:
        # CREATE logica
        item = WatchlistItem(
            watchlistID=watchlist.id,
            titleID=data['titleID'],
            status=data.get('status', 'planned'),
            score=data.get('score'),
            progress=data.get('progress', 0),
            startDate=data.get('startDate'),
            endDate=data.get('endDate'),
            favourite=data.get('favourite', False),
        )
        db.session.add(item)
        created = True

    # Enforce progress logic
    if item.status == "completed":
        max_progress, _ = enforce_progress(item, float('inf'))  # asta returnează maximul calculat (un int)
        item.progress = max_progress
    else:
        orig_progress = item.progress
        new_progress, msg = enforce_progress(item, orig_progress)
        item.progress = new_progress

    # Validare
    if errors := item.validate():
        return jsonify({"errors": errors}), HTTPStatus.BAD_REQUEST

    db.session.commit()
    return jsonify(item.to_dict()), (HTTPStatus.CREATED if created else HTTPStatus.OK)

@watchlist_bp.route('/items/<int:item_id>', methods=['PUT'])
@jwt_required_middleware()
def update_watchlist_item(item_id):
    userID = int(get_jwt_identity())
    data = request.get_json()
    item = WatchlistItem.query.join(Watchlist).filter(
        WatchlistItem.id == item_id,
        Watchlist.userID == userID
    ).first_or_404()

    # Update all fields if present in data
    for field in ['score', 'progress', 'favourite', 'startDate', 'endDate']:
        if field in data:
            setattr(item, field, data[field])

    if 'status' in data:
        item.status = data['status']

    # Progress business logic
    if item.status == "completed":
        max_progress, _ = enforce_progress(item, float('inf'))
        item.progress = max_progress
    elif 'progress' in data:
        orig_progress = data['progress']
        new_progress, msg = enforce_progress(item, orig_progress)
        if new_progress != orig_progress:
            item.progress = new_progress
            return jsonify({"errors": [f"Progress limited: {msg}"]}), HTTPStatus.BAD_REQUEST

    # Validation
    if errors := item.validate():
        return jsonify({"errors": errors}), HTTPStatus.BAD_REQUEST

    db.session.commit()
    return jsonify(item.to_dict()), HTTPStatus.OK

@watchlist_bp.route('/mutual/<int:user1_id>/<int:user2_id>', methods=['GET'])
@jwt_required_middleware()
def get_mutual_watchlist_items(user1_id, user2_id):
    wl1 = Watchlist.query.filter_by(userID=user1_id).first()
    wl2 = Watchlist.query.filter_by(userID=user2_id).first()
    if not wl1 or not wl2:
        return jsonify([]), HTTPStatus.OK

    ids1 = {item.titleID for item in wl1.items}
    ids2 = {item.titleID for item in wl2.items}
    mutual_ids = ids1 & ids2

    mutual_titles = [item.to_dict() for item in wl1.items if item.titleID in mutual_ids]
    return jsonify(mutual_titles), HTTPStatus.OK

@watchlist_bp.route('/items', methods=['GET'])
@jwt_required_middleware()
def get_all_watchlist_items_paginated():
    userID = int(get_jwt_identity())
    watchlist = Watchlist.query.filter_by(userID=userID).first()
    if not watchlist:
        return jsonify({"items": [], "total": 0}), HTTPStatus.OK

    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    query = WatchlistItem.query.filter_by(watchlistID=watchlist.id)
    total = query.count()
    items = query.order_by(WatchlistItem.updated_at.desc()).offset((page - 1) * per_page).limit(per_page).all()

    return jsonify({
        "items": [item.to_dict() for item in items],
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": (total + per_page - 1) // per_page
    }), HTTPStatus.OK

@watchlist_bp.route('/search', methods=['GET'])
@jwt_required_middleware()
def search_watchlist():
    user_id = int(get_jwt_identity())
    q = request.args.get('q', '')
    status = request.args.get('status')
    type_name = request.args.get('type')
    watchlist = Watchlist.query.filter_by(user_id=user_id).first()
    if not watchlist:
        return jsonify({"items": [], "total": 0}), HTTPStatus.OK

    items_query = WatchlistItem.query.join(WatchlistItem.title).filter(
        WatchlistItem.watchlistID == watchlist.id
    )
    if q:
        items_query = items_query.filter(Title.title.ilike(f"%{q}%"))
    if status:
        items_query = items_query.filter(WatchlistItem.status == status)
    if type_name:
        items_query = items_query.join(Title.media_type).filter(
            Type.elementTypeName.ilike(type_name)
        )

    total = items_query.count()
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    items = items_query.order_by(WatchlistItem.updated_at.desc()).offset((page - 1) * per_page).limit(per_page).all()

    return jsonify({
        "items": [item.to_dict() for item in items],
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": (total + per_page - 1) // per_page
    }), HTTPStatus.OK

# @watchlist_bp.route('/export', methods=['GET'])
# @jwt_required_middleware()
# def export_watchlist_csv():
#     user_id = int(get_jwt_identity())
#     watchlist = Watchlist.query.filter_by(user_id=user_id).first()
#     if not watchlist or not watchlist.items:
#         return jsonify({"error": "No items to export"}), HTTPStatus.BAD_REQUEST
#
#     # Transformă datele într-o listă de dict
#     rows = []
#     for item in watchlist.items:
#         rows.append({
#             "id": item.id,
#             "titleID": item.titleID,
#             "titleName": item.title.title if item.title else "",
#             "status": item.status,
#             "score": item.score,
#             "progress": item.progress,
#             "startDate": item.startDate.isoformat() if item.startDate else "",
#             "endDate": item.endDate.isoformat() if item.endDate else "",
#             "favourite": item.favourite
#         })
#
#     # Creează DataFrame și exportă la CSV
#     df = pd.DataFrame(rows)
#     csv_data = df.to_csv(index=False)
#     return Response(
#         csv_data,
#         mimetype='text/csv',
#         headers={"Content-Disposition": "attachment;filename=watchlist.csv"}
#     )
#
# @watchlist_bp.route('/export/xlsx', methods=['GET'])
# @jwt_required_middleware()
# def export_watchlist_xlsx():
#     user_id = int(get_jwt_identity())
#     watchlist = Watchlist.query.filter_by(user_id=user_id).first()
#     if not watchlist or not watchlist.items:
#         return jsonify({"error": "No items to export"}), HTTPStatus.BAD_REQUEST
#
#     rows = [{
#         "id": item.id,
#         "titleID": item.titleID,
#         "titleName": item.title.title if item.title else "",
#         "status": item.status,
#         "score": item.score,
#         "progress": item.progress,
#         "startDate": item.startDate.isoformat() if item.startDate else "",
#         "endDate": item.endDate.isoformat() if item.endDate else "",
#         "favourite": item.favourite
#     } for item in watchlist.items]
#
#     df = pd.DataFrame(rows)
#     output = BytesIO()
#     df.to_excel(output, index=False)
#     output.seek(0)
#     return Response(
#         output.getvalue(),
#         mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
#         headers={"Content-Disposition": "attachment;filename=watchlist.xlsx"}
#     )
#
# @watchlist_bp.route('/export/json', methods=['GET'])
# @jwt_required_middleware()
# def export_watchlist_json():
#     user_id = int(get_jwt_identity())
#     watchlist = Watchlist.query.filter_by(user_id=user_id).first()
#     if not watchlist or not watchlist.items:
#         return jsonify({"error": "No items to export"}), HTTPStatus.BAD_REQUEST
#
#     rows = [{
#         "id": item.id,
#         "titleID": item.titleID,
#         "titleName": item.title.title if item.title else "",
#         "status": item.status,
#         "score": item.score,
#         "progress": item.progress,
#         "startDate": item.startDate.isoformat() if item.startDate else "",
#         "endDate": item.endDate.isoformat() if item.endDate else "",
#         "favourite": item.favourite
#     } for item in watchlist.items]
#
#     df = pd.DataFrame(rows)
#     return Response(
#         df.to_json(orient="records", force_ascii=False, indent=2),
#         mimetype='application/json',
#         headers={"Content-Disposition": "attachment;filename=watchlist.json"}
#     )
# @watchlist_bp.route('/<int:user_id>/taste-graph', methods=['GET'])
# @jwt_required_middleware()
# def taste_graph(user_id):
#     user = User.query.get_or_404(user_id)
#     completed = [item.title.title for item in WatchlistItem.query.join(Watchlist)
#                  .filter(Watchlist.userID == user.id, WatchlistItem.status == 'completed', item.title != None)]
#
#     nodes = []
#     edges = []
#     for base in completed:
#         try:
#             recs = tastedive_recommend(base, limit=3)
#             for rec in recs.get('Similar', {}).get('Results', []):
#                 nodes.append({"id": rec["Name"], "type": rec.get("Type")})
#                 edges.append({"from": base, "to": rec["Name"]})
#         except Exception:
#             continue
#     # Deduplicate nodes
#     node_map = {}
#     for n in nodes:
#         node_map[n['id']] = n
#     return jsonify({
#         "nodes": list(node_map.values()),
#         "edges": edges
#     })

@watchlist_bp.route('/<int:user_id>/recommendations/history', methods=['GET'])
@jwt_required_middleware()
def recommendation_history(user_id):
    user = User.query.get_or_404(user_id)
    completed = [
        item.title.title
        for item in WatchlistItem.query.join(Watchlist)
        .filter(
            Watchlist.userID == user.id,
            WatchlistItem.status == 'completed',
            WatchlistItem.title != None  # Valid if relationship is defined
        )
    ]

    history = []
    for title in completed:
        try:
            recs = tastedive_recommend(title, limit=2)
            history.append({"source": title, "recommendations": recs.get('Similar', {}).get('Results', [])})
        except Exception:
            continue
    return jsonify(history)
