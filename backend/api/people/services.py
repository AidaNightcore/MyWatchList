from datetime import datetime


def update_watch_status(entry, data):
    entry.status = data.get('status', entry.status)
    entry.score = data.get('score', entry.score)
    entry.favourite = data.get('favourite', entry.favourite)

    # Business logic example
    if entry.status == 'Completed' and not entry.endDate:
        entry.endDate = datetime.utcnow().date()