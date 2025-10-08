from flask import Flask, request
from .extensions import db, migrate

# Blueprints
from .routes.auth import bp as auth_bp
from .routes.receipts import bp as receipts_bp
from .routes.items import bp as items_bp

# Config
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)

    from app import models  # Ensure models are imported for migrations

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(receipts_bp, url_prefix="/api/receipts")
    app.register_blueprint(items_bp, url_prefix="/api/items")



    @app.get("/")
    def index():
        return "Landing"

    return app