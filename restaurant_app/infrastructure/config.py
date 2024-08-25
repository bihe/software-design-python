"""Flask config."""

import inspect
import os
from os import path

import yaml


class Config(yaml.YAMLObject):

    # provide the database uri as an "global variable" for later user
    DATABASE_URI = ""
    DATABASE_ECHO = False

    def __init__(self):
        self.SECRET_KEY = ""
        self.STATIC_FOLDER = ""
        self.TEMPLATES_FOLDER = ""
        self.FLASK_ENV = ""
        self.DEBUG = True
        self.TESTING = True
        self.DATABASE_URI = ""
        self.DATABASE_ECHO = False

    def load_from_data(self, data_map):
        for m in dir(self):
            if inspect.ismethod(m):
                continue
            if m in data_map:
                setattr(self, m, data_map[m])

            # overwrite by environment-vars if available
            # note: earlier we have used dotenv to load specific environment variables from an .env file
            env_var = os.getenv(m)
            if env_var is not None and not env_var == "":
                setattr(self, m, env_var)


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
