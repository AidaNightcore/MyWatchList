from datetime import datetime, timezone

from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from api import db


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    username = db.Column(db.String(255), unique=True)
    birthday = db.Column(db.Date)
    profilePicture = db.Column(db.LargeBinary)
    isAdmin = db.Column(db.Boolean, default=False)
    isModerator = db.Column(db.Boolean, default=False)

    lastLogin = db.Column(db.DateTime)
    createdAt = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    # Relationships
    watchlists = relationship('Watchlist', back_populates='user')
    replies = relationship('Reply', back_populates='user')
    relationships_initiated = relationship(
        'UserRelationship',
        foreign_keys='UserRelationship.RelatingUserID',
        back_populates='relating_user'
    )
    relationships_received = relationship(
        'UserRelationship',
        foreign_keys='UserRelationship.RelatedUserID',
        back_populates='related_user'
    )
    refresh_tokens = db.relationship(
        'RefreshToken',
        back_populates='user',
        lazy='dynamic'
    )

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self, include_sensitive=False):
        data = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "username": self.username,
            "birthday": self.birthday.isoformat() if self.birthday else None,
            "profilePicture": bool(self.profilePicture),  # True dacă există
            "isAdmin": self.isAdmin,
            "isModerator": self.isModerator,
            "lastLogin": self.lastLogin.isoformat() if self.lastLogin else None,
            "createdAt": self.createdAt.isoformat() if self.createdAt else None,
        }
        # **NU include parola niciodată**
        if include_sensitive:
            data["password"] = self.password
        return data


class UserRelationship(db.Model):
    __tablename__ = 'UserRelationship'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    RelatingUserID = db.Column(db.Integer, db.ForeignKey('User.id'))
    RelatedUserID = db.Column(db.Integer, db.ForeignKey('User.id'))
    Type = db.Column(db.String(255))

    # Relationships
    relating_user = relationship(
        'User',
        foreign_keys=[RelatingUserID],
        back_populates='relationships_initiated'
    )

    related_user = relationship(
        'User',
        foreign_keys=[RelatedUserID],
        back_populates='relationships_received'
    )

    def to_dict(self):
        return {
            "id": self.id,
            "relating_user_id": self.RelatingUserID,
            "related_user_id": self.RelatedUserID,
            "type": self.Type,
        }


