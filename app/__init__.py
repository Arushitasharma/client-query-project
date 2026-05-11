from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv
import os

from .models import db, User

# LOAD ENV VARIABLES
load_dotenv()

# LOGIN MANAGER
login_manager = LoginManager()


def create_app():

    app = Flask(__name__, instance_relative_config=True)

    # APP CONFIG
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "fallbacksecret"),
        SQLALCHEMY_DATABASE_URI="sqlite:///newsite.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    # DATABASE
    db.init_app(app)

    # LOGIN MANAGER
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please login first"

    # LOAD USER
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # CREATE TABLES
    with app.app_context():
        db.create_all()

    # IMPORT ROUTES
    from .routes.main import main
    from .routes.admin import admin
    from .routes.auth import auth

    # REGISTER BLUEPRINTS
    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(auth)

    return app