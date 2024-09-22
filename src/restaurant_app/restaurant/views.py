from dependency_injector.wiring import Provide, inject
from flask import Blueprint, render_template

from ..auth.views import login_required
from ..infrastructure.cache import Cache
from ..infrastructure.container import Container
from ..infrastructure.logger import LOG
from ..shared.view_helpers import prepare_view_model
from .service import RestaurantService

bp = Blueprint("restaurant", __name__)


@bp.route("/")
@login_required
@inject
def index(
    restaurant_svc: RestaurantService = Provide[Container.restaurant_svc], cache: Cache = Provide[Container.cache]
):
    LOG.info("view restaurant/index")
    restaurants = restaurant_svc.get_all()
    LOG.debug(f"get {len(restaurants)} restaurants")
    model_params = prepare_view_model(cache, restaurants=restaurants)
    return render_template("restaurant/index.html", **model_params)
