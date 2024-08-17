"""Flask config."""

import inspect
import os

import yaml


class Config(yaml.YAMLObject):

    # provide the database uri as an "global variable" for later user
    DATABASE_URI = ""

    def __init__(self):
        self.SECRET_KEY = ""
        self.STATIC_FOLDER = ""
        self.TEMPLATES_FOLDER = ""
        self.FLASK_ENV = ""
        self.DEBUG = True
        self.TESTING = True
        self.DATABASE_URI = ""
        self.FLASK_RUN_HOST = ""
        self.FLASK_RUN_PORT = 0

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
