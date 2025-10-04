from flask import Flask, request
from .extensions import db, migrate
from .routes.user import bp as user_bp
from .routes.internal_testing import bp as internal_testing_bp
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    app.register_blueprint(user_bp, url_prefix="/accounts")
    app.register_blueprint(internal_testing_bp, url_prefix="/internal-testing")


    @app.get("/")
    def index():
        return "Landing"

    return app