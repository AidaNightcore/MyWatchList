from flask import Flask
from flask_migrate import Migrate
from config import Config
from api.common.database import db, init_db
from api.user import routes as user_routes
from api.media import routes as media_routes
from api.social import routes as discussion_routes
from api.people import routes as people_routes

# Import models to register them with SQLAlchemy
from api.user import models as user_models
from api.media import models as media_models
from api.social import models as discussion_models
from api.people import models as people_models

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
init_db(app)
migrate = Migrate(app, db)

# Register blueprints
app.register_blueprint(user_routes.user_bp, url_prefix='/api/users')
app.register_blueprint(media_routes.media_bp, url_prefix='/api/media')
app.register_blueprint(discussion_routes.social_bp, url_prefix='/api/discussions')
app.register_blueprint(people_routes.people_bp, url_prefix='/api/people')

if __name__ == '__main__':
    app.run(debug=True)