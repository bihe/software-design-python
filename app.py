import os
from os import path

from dotenv import load_dotenv
from flask import Flask

from config import config
from restaurant.infrastructure.container import Container
from restaurant.root_views import root_route

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

APPLICATION_NAME = "restaurant-app"


def create_app(app_environment=None):
    app = Flask(APPLICATION_NAME)
    if app_environment is None:
        app_environment = os.getenv("FLASK_ENV", "production")
    app.config.from_object(config[app_environment])

    # dependency injection
    container = Container()
    app.container = container

    # routes via Flask blueprints
    app.register_blueprint(root_route)

    return app


if __name__ == "__main__":
    app = create_app(os.getenv("FLASK_ENV", "production"))
    app.run()
