import os
from logging.config import fileConfig
from os import path
from os.path import abspath

import yaml
from dotenv import load_dotenv
from flask import Flask

from .infrastructure.config import Config

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


def setup_config(base_path, app_environment) -> Config:
    config_file = path.join(base_path, f"{app_environment}_config.yaml")
    if not path.exists(config_file):
        # try just the config.yaml
        config_file = path.join(base_path, "config.yaml")
    if not path.exists(config_file):
        return None

    print("CNF: will load configuration from: %s" % config_file)

    with open(config_file) as f:
        # use safe_load instead load
        data_map = yaml.safe_load(f)
        config = Config()
        config.load_from_data(data_map)
        return config


def create_app():
    basedir = path.abspath(path.dirname(__file__))
    setup_environment(basedir)
    setup_logging(basedir)

    app = Flask(APPLICATION_NAME)
    app_environment = os.getenv("FLASK_ENV", "production")
    print("using environement: %s" % app_environment)
    config = setup_config(basedir, app_environment)
    app.config.from_object(config)

    # set the database uri as a globally available variable
    Config.DATABASE_URI = config.DATABASE_URI

    # dependency injection
    # thie import is not used on the "top" level because
    # otherwis the Container object woutl be instantiated without a proper init of the configuration
    from .infrastructure.container import Container

    container = Container()
    app.container = container

    db = container.db()
    db.create_database()

    # routes via Flask blueprints
    # the same as above, we want to wait for a proper config init until we load the blueprints
    # if done on "top" leve the DI Container would be instantiated without proper configuration
    from .restaurant import root_views

    app.register_blueprint(root_views.bp)
    return app
