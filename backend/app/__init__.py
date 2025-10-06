from flask import Flask, request
from .extensions import db, migrate

# Blueprints
from .routes.auth import bp as auth_bp

from .routes.user import bp as user_bp
from .routes.internal_testing import bp as internal_testing_bp

# Config
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)

    from app import models  # Ensure models are imported for migrations

    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    app.register_blueprint(user_bp, url_prefix="/accounts")
    app.register_blueprint(internal_testing_bp, url_prefix="/internal-testing")


    @app.get("/")
    def index():
        return "Landing"

    return app