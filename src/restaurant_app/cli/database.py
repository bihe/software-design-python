# define a CLI logic for the flask applcation
import os
from pathlib import Path
from typing import List

import click
import marshmallow
from flask import current_app
from flask.cli import AppGroup, with_appcontext
from marshmallow_dataclass import dataclass

from ..infrastructure.config import Config
from ..restaurant.models import AddressModel, RestaurantModel, WeekDay
from ..restaurant.service import RestaurantService
from ..store.database import SqlAlchemyDatbase
from ..store.restaurant_repository import RestaurantRepository

db_cli = AppGroup("db", short_help="Commands to work with the database")


@db_cli.command("create")
@click.argument("filename", required=False)
@with_appcontext  # provide the defined flask application to interact with configuration
def create_database(filename: str):
    if Config.DATABASE_URI.startswith("sqlite"):
        print(f"filename: {filename}")
        if filename is not None:
            file_path = os.path.join("./", filename)
            if not os.path.exists(file_path):
                print(f"SQLITE: the provided filename is not available '{filename}'")
                return

            print(f"SQLITE: delete the database file: '{filename}'")
            os.remove(os.path.join("./", filename))

    print(f"re-create the database using the Url: {Config.DATABASE_URI}")
    db = current_app.container.db()
    db.drop_database()
    db.create_database()


class BaseSchema(marshmallow.Schema):
    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass(base_schema=BaseSchema)
class Address:
    street: str
    city: str
    zip: str
    countryCode: str


@dataclass(base_schema=BaseSchema)
class Table:
    number: str
    places: int


@dataclass(base_schema=BaseSchema)
class Menu:
    name: str
    price: float
    category: str


@dataclass(base_schema=BaseSchema)
class Restaurant:
    name: str
    openDays: List[str]
    openFrom: List[int]
    openUntil: List[int]
    address: Address
    tables: List[Table]
    menus: List[Menu]


@db_cli.command("import")
@click.argument("filename", type=click.Path(exists=True))
@with_appcontext  # provide the defined flask application to interact with configuration
def import_from_json(filename: str):
    # read the file-contents
    json_contents = Path(filename).read_text()
    restaurant: Restaurant = Restaurant.Schema().loads(json_contents)

    # map the open-days
    openDays: List[WeekDay] = []
    for d in restaurant.openDays:
        openDays.append(WeekDay(d))

    # map to RestaurantModel
    restaurant_model = RestaurantModel(
        id=None,
        address=None,
        menus=None,
        tables=None,
        name=restaurant.name,
        openFrom=restaurant.openFrom,
        openUntil=restaurant.openUntil,
        openDays=openDays,
    )

    # map to AddressModel
    address = AddressModel(
        street=restaurant.address.street,
        zip=restaurant.address.zip,
        city=restaurant.address.city,
        countryCode=restaurant.address.countryCode,
    )
    restaurant_model.address = address

    # db: SqlAlchemyDatbase = SqlAlchemyDatbase(db_url=Config.DATABASE_URI, echo=Config.DATABASE_ECHO)

    db: SqlAlchemyDatbase = current_app.container.db()
    print(type(db))
    session = db.get_sessoin()
    repo = RestaurantRepository(session_factory=None, session=session)
    svc: RestaurantService = RestaurantService(repo)
    svc.save(restaurant_model)