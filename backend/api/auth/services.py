import secrets
from datetime import datetime, timedelta
from api.common.database import db
from .models import User, RefreshToken
import re


class AuthService:
    @staticmethod
    def validate_registration(data):
        errors = {}

        if not data.get('name'):
            errors['name'] = "Name is required"

        if not data.get('email'):
            errors['email'] = "Email is required"
        elif not re.match(r'^[^@]+@[^@]+\.[^@]+$', data['email']):
            errors['email'] = "Invalid email format"
        elif User.query.filter_by(email=data['email']).first():
            errors['email'] = "Email already registered"

        if not data.get('username'):
            errors['username'] = "Username is required"
        elif len(data['username']) < 3:
            errors['username'] = "Username must be at least 3 characters"
        elif not data['username'].isalnum():
            errors['username'] = "Username must be alphanumeric"
        elif User.query.filter_by(username=data['username']).first():
            errors['username'] = "Username already taken"

        if not data.get('password'):
            errors['password'] = "Password is required"
        elif len(data['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"

        return errors

    @staticmethod
    def create_user(data):
        new_user = User(
            name=data['name'],
            email=data['email'],
            username=data['username'],
            birthday=data.get('birthday')
        )
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def validate_login(data):
        errors = {}

        if not data.get('password'):
            errors['password'] = "Password is required"

        if not data.get('email') and not data.get('username'):
            errors['credentials'] = "Email or username is required"

        return errors

    @staticmethod
    def authenticate(data):
        if data.get('email'):
            user = User.query.filter_by(email=data['email']).first()
        elif data.get('username'):
            user = User.query.filter_by(username=data['username']).first()
        else:
            return None

        if user and user.check_password(data['password']):
            user.last_login = datetime.utcnow()
            db.session.commit()
            return user
        return None

    @staticmethod
    def create_refresh_token(user):
        RefreshToken.query.filter_by(user_id=user.id).update({"revoked": True})

        token = secrets.token_urlsafe(128)
        expires_at = datetime.utcnow() + timedelta(days=30)

        refresh_token = RefreshToken(
            user_id=user.id,
            token=token,
            expires_at=expires_at
        )
        db.session.add(refresh_token)
        db.session.commit()
        return refresh_token

    @staticmethod
    def revoke_refresh_token(jti):
        token = RefreshToken.query.filter_by(token=jti).first()
        if token:
            token.revoked = True
            db.session.commit()