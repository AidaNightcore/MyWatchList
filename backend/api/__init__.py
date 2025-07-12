from flask import Flask
from .common.database import db
from .common.errors import register_error_handlers
from flask_jwt_extended import JWTManager
from flask_mail import Mail

from .media.routes import admin_bp

mail = Mail()

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)

    # Register error handlers
    register_error_handlers(app)


    mail.init_app(app)

    # Import and register blueprints
    from .auth.routes import auth_bp
    from .media.routes import media_bp
    from .people.routes import people_bp
    from .social.routes import social_bp
    from .user.routes import user_bp
    from .watchlist.routes import watchlist_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(media_bp)
    app.register_blueprint(people_bp)
    app.register_blueprint(social_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(watchlist_bp)
    app.register_blueprint(admin_bp)

    return app