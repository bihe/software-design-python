from dependency_injector.wiring import Provide, inject
from flask import Blueprint

from restaurant.infrastructure.container import Container
from restaurant.services.restaurant import RestaurantService

root_route = Blueprint("root", __name__)


@root_route.route("/")
@inject
def hello(restaurant_svc: RestaurantService = Provide[Container.restaurant_svc]):
    return "this hello-world handler uses the service: %s" % (restaurant_svc.get_service_name())
