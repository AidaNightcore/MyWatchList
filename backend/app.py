import redis
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from api.common.database import db, init_db
from api.media.routes import media_bp, admin_bp
from api.user.models import User
from config import Config
import logging
from api import create_app



# Create application instance
app = create_app(Config)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)