import os
from os import path

from flask import Flask

from .cli import db_cli
from .infrastructure.config import Config, setup_config
from .infrastructure.environment import setup_environment
from .infrastructure.logger import setup_logging


def create_app():
    basedir = path.abspath(path.dirname(__file__))
    setup_environment(basedir)
    setup_logging(basedir)

    app = Flask("restaurant-app")
    app_environment = os.getenv("FLASK_ENV", "production")
    print("using environement: %s" % app_environment)
    config = setup_config(basedir, app_environment)
    app.config.from_object(config)

    # add the logic to enable cli commands
    app.cli.add_command(db_cli)

    # set the database uri as a globally available variable
    Config.DATABASE_URI = config.DATABASE_URI

    # dependency injection
    # this import is not used on the "top" level because
    # otherwis the Container object woutl be instantiated without a proper init of the configuration
    from .infrastructure.container import Container

    container = Container()
    app.container = container

    # routes via Flask blueprints
    # the same as above, we want to wait for a proper config init until we load the blueprints
    from .restaurant import root_views

    app.register_blueprint(root_views.bp)
    return app
