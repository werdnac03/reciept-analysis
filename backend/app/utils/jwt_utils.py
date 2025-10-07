import jwt
from datetime import datetime, timedelta
from flask import current_app, request, jsonify
from functools import wraps

def create_token(user_id):
    payload = {
        "user_id": user_id,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=6)
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

def verify_token(token):
    try:
        return jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return jsonify({"error": "Token missing"}), 401

        data = verify_token(token)
        if not data:
            return jsonify({"error": "Invalid or expired token"}), 401

        return f(data["user_id"], *args, **kwargs)
    return decorated
