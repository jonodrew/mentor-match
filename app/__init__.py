from flask import Flask

from app.config import Config


def create_app(configuration=Config):
    app = Flask(__name__, static_folder="static")

    app.config.from_object(configuration)

    from app.main import main_bp

    app.register_blueprint(main_bp)

    return app
