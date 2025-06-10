from datetime import datetime
from http import HTTPStatus
from flask import jsonify


def validate_watchlist_item(data):
    errors = []

    # Required fields
    if 'title_id' not in data:
        errors.append("title_id is required")

    # Status validation
    valid_statuses = ['watching', 'completed', 'on_hold', 'dropped', 'planned']
    if 'status' in data and data['status'] not in valid_statuses:
        errors.append(f"status must be one of: {', '.join(valid_statuses)}")

    # Score validation
    if 'score' in data and (not isinstance(data['score'], (int, float)) or data['score'] < 1 or data['score'] > 10):
        errors.append("score must be between 1-10")

    # Date validation
    try:
        if 'start_date' in data:
            datetime.fromisoformat(data['start_date'])
        if 'end_date' in data:
            datetime.fromisoformat(data['end_date'])
    except ValueError:
        errors.append("dates must be in ISO format (YYYY-MM-DD)")

    return errors