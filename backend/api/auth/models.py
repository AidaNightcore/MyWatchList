from datetime import datetime
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash
import re
from api import db

from api.user.models import User

def enhance_user_model():

    if not hasattr(User, 'validate_email'):
        @validates('email')
        def validate_email(self, key, email):
            if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
                raise ValueError("Invalid email format")
            return email

        User.validate_email = validate_email

    if not hasattr(User, 'validate_username'):
        @validates('username')
        def validate_username(self, key, username):
            if len(username) < 3:
                raise ValueError("Username must be at least 3 characters")
            if not username.isalnum():
                raise ValueError("Username must be alphanumeric")
            return username

        User.validate_username = validate_username

    if not hasattr(User, 'set_password'):
        def set_password(self, password):
            if len(password) < 8:
                raise ValueError("Password must be at least 8 characters")
            self.password = generate_password_hash(password)

        User.set_password = set_password

    if not hasattr(User, 'check_password'):
        def check_password(self, password):
            return check_password_hash(self.password, password)

        User.check_password = check_password

    if not hasattr(User, 'to_dict'):
        def to_dict(self):
            return {
                'id': self.id,
                'name': self.name,
                'email': self.email,
                'username': self.username
            }

        User.to_dict = to_dict

enhance_user_model()

class RefreshToken(db.Model):
    __tablename__ = 'RefreshToken'

    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('User.id'))
    token = db.Column(db.String(512), unique=True)
    expiresAt = db.Column(db.DateTime)
    revoked = db.Column(db.Boolean, default=False)

    # Relationship
    user = db.relationship('User', back_populates='refresh_tokens')

    def is_valid(self):
        from datetime import datetime
        return not self.revoked and datetime.utcnow() < self.expires_at