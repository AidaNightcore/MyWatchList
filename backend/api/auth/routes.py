from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from http import HTTPStatus
from .models import User, RefreshToken
from .services import AuthService
from api.middleware import jwt_required_middleware

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), HTTPStatus.BAD_REQUEST

    if errors := AuthService.validate_registration(data):
        return jsonify({"errors": errors}), HTTPStatus.BAD_REQUEST

    try:
        user = AuthService.create_user(data)
        return jsonify({
            "message": "User created successfully",
            "user": user.to_dict()
        }), HTTPStatus.CREATED
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), HTTPStatus.BAD_REQUEST

    if errors := AuthService.validate_login(data):
        return jsonify({"errors": errors}), HTTPStatus.BAD_REQUEST

    user = AuthService.authenticate(data)
    if not user:
        return jsonify({"error": "Invalid credentials"}), HTTPStatus.UNAUTHORIZED

    access_token = create_access_token(identity=user)
    refresh_token = AuthService.create_refresh_token(user)

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token.token,
        "user": user.to_dict()
    }), HTTPStatus.OK

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user or not user.is_active:
        return jsonify({"error": "Invalid user"}), HTTPStatus.UNAUTHORIZED

    jti = get_jwt()["jti"]
    AuthService.revoke_refresh_token(jti)

    new_access_token = create_access_token(identity=user.id)
    new_refresh_token = AuthService.create_refresh_token(user)

    return jsonify({
        "access_token": new_access_token,
        "refresh_token": new_refresh_token.token
    }), HTTPStatus.OK

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    AuthService.revoke_refresh_token(jti)
    return jsonify({"message": "Successfully logged out"}), HTTPStatus.OK