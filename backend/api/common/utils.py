from sqlalchemy import func, distinct
from sqlalchemy.orm import joinedload

from api.media.models import Show, Season, Episode, Title, Movie, Book
from api.watchlist.models import WatchlistItem
from api.common.database import db

def get_score_recursive(element_type, element_id):
    if element_type == 'Episode':
        watch_elements = WatchlistItem.query.filter_by(titleID=element_id).all()
        scores = [we.score for we in watch_elements if we.score is not None]
        return sum(scores) / len(scores) if scores else None

    elif element_type == 'Season':
        season = Season.query.options(joinedload(Season.episodes)).get(element_id)
        if not season or not season.episodes:
            return None
        episode_scores = [
            get_score_recursive('Episode', ep.id)
            for ep in season.episodes
        ]
        episode_scores = [s for s in episode_scores if s is not None]
        return sum(episode_scores) / len(episode_scores) if episode_scores else None

    elif element_type == 'Show':
        show = Show.query.options(joinedload(Show.seasons)).get(element_id)
        if not show or not show.seasons:
            return None
        season_scores = [
            get_score_recursive('Season', sz.id)
            for sz in show.seasons
        ]
        season_scores = [s for s in season_scores if s is not None]
        return sum(season_scores) / len(season_scores) if season_scores else None

    elif element_type == 'Movie':
        watch_elements = WatchlistItem.query.filter_by(titleID=element_id).all()
        scores = [we.score for we in watch_elements if we.score is not None]
        return sum(scores) / len(scores) if scores else None

    elif element_type == 'Book':
        watch_elements = WatchlistItem.query.filter_by(titleID=element_id).all()
        scores = [we.score for we in watch_elements if we.score is not None]
        return sum(scores) / len(scores) if scores else None

    return None


def get_movies_with_aggregated_score():
    results = db.session.query(
        Movie,
        func.avg(WatchlistItem.score).label("avg_score")
    ).join(Title, Title.id == Movie.typeID) \
     .outerjoin(WatchlistItem, WatchlistItem.titleID == Title.id) \
     .group_by(Movie.id) \
     .order_by(func.avg(WatchlistItem.score).desc().nullslast()) \
     .all()
    return results

def get_books_with_aggregated_score():
    results = db.session.query(
        Book,
        func.avg(WatchlistItem.score).label("avg_score")
    ).join(Title, Title.id == Book.typeID) \
     .outerjoin(WatchlistItem, WatchlistItem.titleID == Title.id) \
     .group_by(Book.id) \
     .order_by(func.avg(WatchlistItem.score).desc().nullslast()) \
     .all()
    return results

