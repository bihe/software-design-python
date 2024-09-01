from dependency_injector.wiring import Provide, inject
from flask import Blueprint

from ..infrastructure.container import Container
from ..infrastructure.logger import LOG
from .service import RestaurantService

bp = Blueprint("root", __name__)


@bp.route("/")
@inject
def hello(restaurant_svc: RestaurantService = Provide[Container.restaurant_svc]):
    LOG.debug("A debug message")
    return f"this hello-world handler uses the service: {restaurant_svc}"
