# import os

from dependency_injector import containers, providers

from ..restaurant.service import RestaurantService
from ..store.database import SqlAlchemyDatbase
from ..store.restaurant_repository import RestaurantRepository
from .config import Config


class Container(containers.DeclarativeContainer):

    # https://python-dependency-injector.ets-labs.org/wiring.html#making-injections-into-modules-and-class-attributes
    wiring_config = containers.WiringConfiguration(packages=[__name__, "..restaurant.root_views", "..cli.database"])
    db = providers.Singleton(SqlAlchemyDatbase, db_url=Config.DATABASE_URI, echo=Config.DATABASE_ECHO)
    restaurant_repo = providers.Factory(RestaurantRepository, session_factory=db.provided.session)
    restaurant_svc = providers.Factory(RestaurantService, repo=restaurant_repo)
