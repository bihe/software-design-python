import os
from os import path

from flask import Flask, redirect, url_for

from .cli.database import db_cli
from .infrastructure.config import Config, setup_config
from .infrastructure.environment import setup_environment
from .infrastructure.logger import LOG, setup_logging
from .shared.view_helpers import UserCacheMissError


def handle_user_cache_miss(e: Exception):
    """if there is no user in the cache, show the login again!"""
    LOG.error(f"{e}")
    return redirect(url_for("auth.show_login"))


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

    # set database seetings as a globally available variables
    Config.DATABASE_URI = config.DATABASE_URI
    Config.DATABASE_ECHO = config.DATABASE_ECHO

    # dependency injection
    # this import is not used on the "top" level because
    # otherwise the Container object woutl be instantiated without a proper init of the configuration
    from .infrastructure.container import Container

    container = Container()
    app.container = container

    # register error handlers
    app.register_error_handler(UserCacheMissError, handle_user_cache_miss)

    # routes via Flask blueprints
    # the same as above, we want to wait for a proper config init until we load the blueprints
    from .restaurant import views as restaurant_views

    app.register_blueprint(restaurant_views.bp)

    from .auth import views as auth_views

    app.register_blueprint(auth_views.bp)

    return app
