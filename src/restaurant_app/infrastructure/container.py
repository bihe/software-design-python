# import os

from dependency_injector import containers, providers

from ..restaurant.service import RestaurantService
from ..store.database import SqlAlchemyDatbase
from ..store.menu_repository import MenuRepository
from ..store.restaurant_repository import RestaurantRepository
from ..store.table_repository import TableRepository
from .config import Config
from .memory_cache import MemoryCache


class Container(containers.DeclarativeContainer):

    # https://python-dependency-injector.ets-labs.org/wiring.html#making-injections-into-modules-and-class-attributes
    wiring_config = containers.WiringConfiguration(packages=[__name__, "..restaurant.views", "..auth.views"])
    db = providers.Singleton(SqlAlchemyDatbase, db_url=Config.DATABASE_URI, echo=Config.DATABASE_ECHO)

    # define the factories for the repositories
    restaurant_repo = providers.Factory(RestaurantRepository, session_factory=db.provided.managed_session)
    menu_repo = providers.Factory(MenuRepository, session_factory=db.provided.managed_session)
    table_repo = providers.Factory(TableRepository, session_factory=db.provided.managed_session)

    # define a cache
    cache = providers.Singleton(MemoryCache)

    # define and wire the needed dependencies for services
    restaurant_svc = providers.Factory(
        RestaurantService, restaurant_repo=restaurant_repo, menu_repo=menu_repo, table_repo=table_repo
    )
