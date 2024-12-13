# import os

from dependency_injector import containers, providers

from ..reservation.service import ReservationService
from ..restaurant.service import RestaurantService
from ..store.database import SqlAlchemyDatabase
from ..store.menu_repository import MenuRepository
from ..store.reservation_repo import ReservationRepository
from ..store.restaurant_repository import RestaurantRepository
from ..store.table_repository import TableRepository
from .config import Config
from .memory_cache import MemoryCache


class Container(containers.DeclarativeContainer):

    # https://python-dependency-injector.ets-labs.org/wiring.html#making-injections-into-modules-and-class-attributes
    # this configuration tells the dependency-injection framework where to "expect" the @inject annotation
    # use python package paths (relative ones), to specify in which files (views) the @inject annotation is used
    wiring_config = containers.WiringConfiguration(
        packages=[__name__, "..restaurant.views", "..auth.views", "..reservation.views"]
    )
    db = providers.Singleton(SqlAlchemyDatabase, db_url=Config.DATABASE_URI, echo=Config.DATABASE_ECHO)

    # define the factories for the repositories
    restaurant_repo = providers.Factory(RestaurantRepository, session_factory=db.provided.managed_session)
    menu_repo = providers.Factory(MenuRepository, session_factory=db.provided.managed_session)
    table_repo = providers.Factory(TableRepository, session_factory=db.provided.managed_session)
    reservation_repo = providers.Factory(ReservationRepository, session_factory=db.provided.managed_session)

    # define a cache
    cache = providers.Singleton(MemoryCache)

    # define and wire the needed dependencies for services
    restaurant_svc = providers.Factory(
        RestaurantService, restaurant_repo=restaurant_repo, menu_repo=menu_repo, table_repo=table_repo
    )
    reservation_svc = providers.Factory(
        ReservationService, restaurant_svc=restaurant_svc, reservation_repo=reservation_repo, table_repo=table_repo
    )
