from flask import Blueprint, request, jsonify

bp = Blueprint("accounts", __name__)


@bp.post("/auth/login")
def login():
    email = request.json.get("email")
    password = request.json.get("password")
    #user = User.query.filter_by(email=email).first()
    return jsonify({"ok": True, "user": {"token": "fake-jwt-token"}}), 200
    #if not user or not user.check_password(password):
    #    return jsonify({"ok": False, "errors": ["Invalid email or password"]}), 401
    #return jsonify({"ok": True, "user": {"id": user.id, "email": user.email}}), 200