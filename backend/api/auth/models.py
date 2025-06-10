from datetime import datetime
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash
import re
from api import db

# Import your existing User model
from api.user.models import User


# Extend the existing User model with authentication features
def enhance_user_model():
    # Add new columns if they don't exist
    if not hasattr(User, 'created_at'):
        User.created_at = db.Column(db.DateTime, default=datetime.utcnow)

    if not hasattr(User, 'last_login'):
        User.last_login = db.Column(db.DateTime)

    if not hasattr(User, 'is_active'):
        User.is_active = db.Column(db.Boolean, default=True)

    if not hasattr(User, 'is_admin'):
        User.is_admin = db.Column(db.Boolean, default=False)

    # Add refresh token relationship
    if not hasattr(User, 'refresh_tokens'):
        User.refresh_tokens = db.relationship(
            'RefreshToken',
            back_populates='user',
            lazy='dynamic'
        )

    # Add validators if they don't exist
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

    # Add password methods
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
                'username': self.username,
                'is_active': self.is_active
            }

        User.to_dict = to_dict


# Call this function to enhance the User model
enhance_user_model()


# Define the RefreshToken model
class RefreshToken(db.Model):
    __tablename__ = 'refresh_token'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    token = db.Column(db.String(512), unique=True)
    expires_at = db.Column(db.DateTime)
    revoked = db.Column(db.Boolean, default=False)

    # Relationship
    user = db.relationship('User', back_populates='refresh_tokens')

    def is_valid(self):
        from datetime import datetime
        return not self.revoked and datetime.utcnow() < self.expires_at