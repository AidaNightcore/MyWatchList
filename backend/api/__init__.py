import redis
from flask import Flask, jsonify
from flask_cors import CORS

from .common.database import db, init_db
from .common.errors import register_error_handlers
from flask_jwt_extended import JWTManager
from flask_mail import Mail

from .media.routes import admin_bp
import logging
from .user.models import User

mail = Mail()

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    init_db(app)  # Initialize database first
    jwt = JWTManager(app)
    CORS(app)  # Enable CORS

    redis_client = redis.from_url(app.config['REDIS_URL'])

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Import models AFTER initializing db
    from api.auth.models import RefreshToken
    from api.media.models import (
        Book, Movie, Show, Season, Episode,
        Title, Genre, Franchise, Publisher, Type
    )
    from api.people.models import Worker, Job, Crew
    from api.social.models import Topic, Reply
    from api.user.models import UserRelationship
    from api.watchlist.models import Watchlist, WatchlistItem

    # Register blueprints
    from api.auth.models import enhance_user_model
    from api.auth.routes import auth_bp
    from api.media.routes import media_bp
    from api.people.routes import people_bp
    from api.social.routes import social_bp
    from api.user.routes import user_bp
    from api.watchlist.routes import watchlist_bp

    enhance_user_model()
    app.register_blueprint(auth_bp)
    app.register_blueprint(media_bp)
    app.register_blueprint(people_bp)
    app.register_blueprint(social_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(watchlist_bp)
    app.register_blueprint(admin_bp)

    # JWT configuration
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        token = RefreshToken.query.filter_by(token=jti).first()
        return token is not None and token.revoked

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return str(user.id)  # always return string

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = int(jwt_data["sub"])
        return User.query.get(identity)

    # Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad request"}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({"error": "Unauthorized"}), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500

    # Database health check
    @app.route('/health')
    def health_check():
        try:
            db.session.execute('SELECT 1')
            return jsonify({"status": "healthy"}), 200
        except Exception:
            return jsonify({"status": "unhealthy"}), 500

    # Register error handlers
    register_error_handlers(app)

    mail.init_app(app)
    return app
