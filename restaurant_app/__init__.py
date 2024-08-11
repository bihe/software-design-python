import os
from logging.config import fileConfig
from os import path
from os.path import abspath

from dotenv import load_dotenv
from flask import Flask

from .config import config
from .infrastructure.container import Container
from .restaurant import root_views

APPLICATION_NAME = "restaurant-app"


def setup_environment(base_path):
    # find the .env files
    env_path = path.join(base_path, ".env")
    if path.exists(env_path):
        print("ENV: will load environment from: %s" % env_path)
        load_dotenv(env_path)
        print()
        return

    # also try to find a file in the parent dir
    env_path = abspath(path.join(base_path, "../", ".env"))
    if path.exists(env_path):
        print("ENV: will load environment from: %s" % env_path)
        load_dotenv(env_path)
        return


def setup_logging(base_path):
    config_file = path.join(base_path, "logger.ini")
    if path.exists(config_file):
        print("LOG: will load logging configuration from: %s" % config_file)
        fileConfig(config_file)
        return

    # try to use the path defined in the file LOGGING_CONFIG_PATH
    config_file = os.getenv("LOGGING_CONFIG_PATH")
    if config_file and not config_file == "":
        print("LOG: logging configuration from LOGGING_CONFIG_PATH: %s" % config_file)
        fileConfig(config_file)
        return


def create_app():
    basedir = path.abspath(path.dirname(__file__))
    setup_environment(basedir)
    setup_logging(basedir)

    app = Flask(APPLICATION_NAME)
    app_environment = os.getenv("FLASK_ENV", "production")
    print("using environement: %s" % app_environment)
    app.config.from_object(config[app_environment])

    # dependency injection
    container = Container()
    app.container = container

    # routes via Flask blueprints
    app.register_blueprint(root_views.bp)
    return app
