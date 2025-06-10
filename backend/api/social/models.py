
from sqlalchemy.orm import relationship

from api import db


class Topic(db.Model):
    __tablename__ = 'Topic'
    id = db.Column(db.Integer, primary_key=True)
    titleID = db.Column(db.Integer, db.ForeignKey('Titles.id'))

    # Relationships
    title = relationship('Title', back_populates='topics')
    replies = relationship('Reply', back_populates='topic')


class Reply(db.Model):
    __tablename__ = 'Reply'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topicID = db.Column(db.Integer, db.ForeignKey('Topic.id'))
    message = db.Column(db.String(255))
    userID = db.Column(db.Integer, db.ForeignKey('User.id'))
    date = db.Column(db.Date)

    # Relationships
    topic = relationship('Topic', back_populates='replies')
    user = relationship('User', back_populates='replies')