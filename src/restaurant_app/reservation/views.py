from dependency_injector.wiring import Provide, inject
from flask import Blueprint, render_template, request

from ..auth.views import login_required
from ..infrastructure.cache import Cache
from ..infrastructure.container import Container
from ..infrastructure.logger import LOG
from ..restaurant.models import RestaurantModel
from ..restaurant.service import RestaurantService
from ..shared.hash import valid_hash_supplied
from ..shared.view_helpers import get_restaurants_from_cache, prepare_view_model, put_restaurants_to_cache
from .forms import ReservationForm
from .service import ReservationService

bp = Blueprint("reservation", __name__)


def restaurant_from_cache(cache: Cache, restaurant_id: int) -> RestaurantModel:
    restaurants = get_restaurants_from_cache(cache)
    restaurant = next(filter(lambda x: x.id == restaurant_id, restaurants))
    return restaurant


@bp.get("/reservation")
@login_required
@inject
def index(
    restaurant_svc: RestaurantService = Provide[Container.restaurant_svc], cache: Cache = Provide[Container.cache]
):
    LOG.info("view reservation/index")
    restaurants = restaurant_svc.get_all()
    LOG.debug(f"got {len(restaurants)} restaurants")
    if restaurants is not None and len(restaurants) > 0:
        put_restaurants_to_cache(cache, restaurants)

    model_params = prepare_view_model(cache, restaurants=restaurants)
    return render_template("reservation/index.html", **model_params)


@bp.get("/reservation/partial/~reservations")
@login_required
@inject
def partial_reservations(
    reservation_svc: ReservationService = Provide[Container.reservation_svc], cache: Cache = Provide[Container.cache]
):
    LOG.info("view reservation/partial_reservations")
    restaurant_id = request.args.get("restaurant_id", "")
    if restaurant_id is None or restaurant_id == "":
        return ""

    restaurant = restaurant_from_cache(cache, int(restaurant_id))
    reservations = reservation_svc.get_reservation_for_restaurant(restaurant_id)
    LOG.debug(f"got {len(reservations)} reservations")
    return render_template("reservation/partial/reservation.html", reservations=reservations, restaurant=restaurant)


@bp.get("/reservation/partial/~reservation-form")
@login_required
@inject
def partial_reservation_form(
    reservation_svc: ReservationService = Provide[Container.reservation_svc], cache: Cache = Provide[Container.cache]
):
    LOG.info("view reservation/partial_reservation_form")
    restaurant_id = request.args.get("restaurant_id", "")
    restaurant_id_hash = request.args.get("h", "")
    valid_hash_supplied(restaurant_id, restaurant_id_hash)

    restaurant = restaurant_from_cache(cache, int(restaurant_id))
    form = ReservationForm(data={"restaurant_id": restaurant_id, "h": restaurant_id_hash})
    return render_template("reservation/partial/reservation_form.html", restaurant=restaurant, form=form)


@bp.get("/reservation/partial/~reservation-save")
@login_required
@inject
def save(
    reservation_svc: ReservationService = Provide[Container.reservation_svc], cache: Cache = Provide[Container.cache]
):
    return ""
