from datetime import datetime

from sqlalchemy import CheckConstraint

from api import db


class Watchlist(db.Model):
    __tablename__ = 'Watchlist'
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='watchlists')
    items = db.relationship('WatchlistItem', back_populates='watchlist', cascade='all, delete-orphan')


class WatchlistItem(db.Model):
    __tablename__ = 'WatchElement'
    id = db.Column(db.Integer, primary_key=True)
    watchlistID = db.Column(db.Integer, db.ForeignKey('Watchlist.id'), nullable=False)
    titleID = db.Column(db.Integer, db.ForeignKey('Titles.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='planned')
    score = db.Column(db.Float)
    progress = db.Column(db.Integer, default=0)
    startDate = db.Column(db.Date)
    endDate = db.Column(db.Date)
    favourite = db.Column('favourite', db.Boolean, default=False)

    # Relationships
    watchlist = db.relationship('Watchlist', back_populates='items')
    title = db.relationship(
        'Title',
        back_populates = 'watch_elements'
    )

    __table_args__ = (
        CheckConstraint('status IN ("watching", "completed", "on_hold", "dropped", "planned")',
                        name='valid_status'),
        CheckConstraint('score IS NULL OR (score >= 1 AND score <= 10)',
                        name='valid_score'),
        CheckConstraint('progress >= 0', name='non_negative_progress'),
        db.UniqueConstraint('watchlistID', 'titleID', name='unique_watchlist_item'),
    )

    def validate(self):

        errors = []

        if self.status not in ['watching', 'completed', 'on_hold', 'dropped', 'planned']:
            errors.append("Invalid status value")

        if self.score and (self.score < 1 or self.score > 10):
            errors.append("Score must be between 1-10")

        if self.progress < 0:
            errors.append("Progress can't be negative")

        if self.startDate and self.endDate and self.startDate > self.endDate:
            errors.append("End date cannot be before start date")

        return errors

    def to_dict(self):
        return {
            'id': self.id,
            'titleID': self.titleID,
            'status': self.status,
            'score': self.score,
            'progress': self.progress,
            'startDate': self.startDate.isoformat() if self.startDate else None,
            'endDate': self.endDate.isoformat() if self.endDate else None,
            'favourite': self.favourite,
            'title': {
                'id': self.title.id,
                'name': self.title.title
            } if self.title else None
        }