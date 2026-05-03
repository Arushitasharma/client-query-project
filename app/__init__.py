from flask import Flask
from .database import init_db

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY="supersecretkey"  # required for session
    )

    init_db(app)

    from .routes.main import main
    from .routes.admin import admin
    from .routes.auth import auth

    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(auth)

    return app