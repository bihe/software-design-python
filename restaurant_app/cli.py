# define a CLI logic for the flask applcation
# a main command "db" with sub-commands "create"
import os

from flask import current_app
from flask.cli import AppGroup, with_appcontext

from .infrastructure.config import Config

db_cli = AppGroup("db", short_help="Commands to work with the database")


@db_cli.command("create")
@with_appcontext  # provide the defined flask application to interact with configuration
def create_database():
    if Config.DATABASE_URI.startswith("sqlite"):
        print("delete the database file: 'app.db'")
        os.remove("./app.db")

    print(f"re-create the database using the Url: {Config.DATABASE_URI}")
    db = current_app.container.db()
    db.drop_database()
    db.create_database()
