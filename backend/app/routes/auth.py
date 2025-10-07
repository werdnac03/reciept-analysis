from flask import Blueprint, request, jsonify
from app import db
from app.models.models import User
from app.utils.jwt_utils import create_token, token_required

bp = Blueprint("auth", __name__)


@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    if not email or not username or not password:
        return jsonify({"error": "Missing fields"}), 400

    # check if email or username already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username taken"}), 400

    # create and save new user
    user = User(email=email, username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing credentials"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401
    token = create_token(user.user_id)

    return jsonify({
        "token": token,
        "user": {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email
        }
    }), 200


@bp.route("/logout", methods=["POST"])
@token_required
def logout(user_id):
    # JWT logout handled client-side by deleting token
    return jsonify({"message": "Logged out"}), 200
