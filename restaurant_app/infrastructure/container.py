from dependency_injector import containers, providers

from ..restaurant.services.restaurant import RestaurantService


class Container(containers.DeclarativeContainer):
    # https://python-dependency-injector.ets-labs.org/wiring.html#making-injections-into-modules-and-class-attributes
    wiring_config = containers.WiringConfiguration(packages=[__name__, "..restaurant.root_views"])

    restaurant_svc = providers.Singleton(RestaurantService)
