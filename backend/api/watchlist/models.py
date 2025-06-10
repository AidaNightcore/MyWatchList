from datetime import datetime

from sqlalchemy import CheckConstraint

from api import db


class Watchlist(db.Model):
    __tablename__ = 'Watchlist'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='watchlists')
    items = db.relationship('WatchlistItem', back_populates='watchlist', cascade='all, delete-orphan')


class WatchlistItem(db.Model):
    __tablename__ = 'WatchElement'
    id = db.Column(db.Integer, primary_key=True)
    watchlist_id = db.Column(db.Integer, db.ForeignKey('Watchlist.id'), nullable=False)
    title_id = db.Column(db.Integer, db.ForeignKey('Titles.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='planned')
    score = db.Column(db.Float)
    progress = db.Column(db.Integer, default=0)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    is_favorite = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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
        db.UniqueConstraint('watchlist_id', 'title_id', name='unique_watchlist_item'),
    )

    def validate(self):

        errors = []

        if self.status not in ['watching', 'completed', 'on_hold', 'dropped', 'planned']:
            errors.append("Invalid status value")

        if self.score and (self.score < 1 or self.score > 10):
            errors.append("Score must be between 1-10")

        if self.progress < 0:
            errors.append("Progress can't be negative")

        if self.start_date and self.end_date and self.start_date > self.end_date:
            errors.append("End date cannot be before start date")

        return errors

    def to_dict(self):
        return {
            'id': self.id,
            'title_id': self.title_id,
            'status': self.status,
            'score': self.score,
            'progress': self.progress,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_favorite': self.is_favorite,
            'notes': self.notes,
            'title': {
                'id': self.title.id,
                'name': self.title.title
            } if self.title else None
        }