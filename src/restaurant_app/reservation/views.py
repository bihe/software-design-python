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
from .models import ReservationRequestModel
from .service import ReservationError, ReservationService

bp = Blueprint("reservation", __name__)


def restaurant_from_cache(cache: Cache, restaurant_id: int, restaurant_svc: RestaurantService) -> RestaurantModel:
    restaurants = get_restaurants_from_cache(cache)
    if restaurants is None or len(restaurants) == 0:
        # reload restaurant from DB
        restaurants = restaurant_svc.get_all()
        if restaurants is not None and len(restaurants) > 0:
            put_restaurants_to_cache(cache, restaurants)
        restaurant = restaurant_svc.get_by_id(restaurant_id)
    else:
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
    restaurant_svc: RestaurantService = Provide[Container.restaurant_svc],
    reservation_svc: ReservationService = Provide[Container.reservation_svc],
    cache: Cache = Provide[Container.cache],
):
    LOG.info("view reservation/partial_reservations")
    restaurant_id = request.args.get("restaurant_id", "")
    if restaurant_id is None or restaurant_id == "":
        return ""

    restaurant = restaurant_from_cache(cache, int(restaurant_id), restaurant_svc)
    reservations = reservation_svc.get_reservation_for_restaurant(restaurant_id)
    LOG.debug(f"got {len(reservations)} reservations")
    return render_template("reservation/partial/reservation.html", reservations=reservations, restaurant=restaurant)


@bp.get("/reservation/partial/~reservation-form")
@login_required
@inject
def partial_reservation_form(
    restaurant_svc: RestaurantService = Provide[Container.restaurant_svc], cache: Cache = Provide[Container.cache]
):
    LOG.info("view reservation/partial_reservation_form")
    restaurant_id = request.args.get("restaurant_id", "")
    restaurant_id_hash = request.args.get("h", "")
    valid_hash_supplied(restaurant_id, restaurant_id_hash)

    restaurant = restaurant_from_cache(cache, int(restaurant_id), restaurant_svc)
    form = ReservationForm(data={"restaurant_id": restaurant_id, "h": restaurant_id_hash})
    return render_template("reservation/partial/reservation_form.html", restaurant=restaurant, form=form)


@bp.post("/reservation/partial/~reservation-save")
@login_required
@inject
def save(
    restaurant_svc: RestaurantService = Provide[Container.restaurant_svc],
    reservation_svc: ReservationService = Provide[Container.reservation_svc],
    cache: Cache = Provide[Container.cache],
):
    restaurant_id = request.form["restaurant_id"]
    restaurant_id_hash = request.form["h"]
    valid_hash_supplied(restaurant_id, restaurant_id_hash)
    restaurant = restaurant_from_cache(cache, int(restaurant_id), restaurant_svc)

    form: ReservationForm = ReservationForm(request.form)
    if not form.validate():
        # some of the model-validation did not work out, show the form again!
        return render_template("reservation/partial/reservation_form.html", restaurant=restaurant, form=form)

    try:
        reservation = reservation_svc.reserve(
            ReservationRequestModel(
                restaurant_id=int(restaurant_id),
                name=form.name.data,
                num_people=form.num_people.data,
                time_from=form.time_from.data,
                time_until=form.time_until.data,
                reservation_date=form.reservation_date.data,
            )
        )
    except ReservationError as res_error:
        LOG.info(f"could not place a reservation '{res_error}'")
        # show the form again and display the reason for not being able to place reservation
        return render_template(
            "reservation/partial/reservation_form.html", restaurant=restaurant, form=form, reservation_error=res_error
        )

    LOG.info(f"create a reservation for '{reservation.name}' on the '{reservation.reservation_date}'")

    # fetch the reservations again
    reservations = reservation_svc.get_reservation_for_restaurant(restaurant_id)
    LOG.debug(f"got {len(reservations)} reservations")
    return render_template("reservation/partial/reservation.html", reservations=reservations, restaurant=restaurant)


@bp.delete("/reservation/partial/<restaurant_id>/<reservation_id>")
@login_required
@inject
def delete(
    restaurant_id: int,
    reservation_id: int,
    restaurant_svc: RestaurantService = Provide[Container.restaurant_svc],
    reservation_svc: ReservationService = Provide[Container.reservation_svc],
    cache: Cache = Provide[Container.cache],
):
    restaurant = restaurant_from_cache(cache, int(restaurant_id), restaurant_svc)

    try:
        reservation_svc.delete(reservation_id)
        reservations = reservation_svc.get_reservation_for_restaurant(restaurant_id)
        LOG.debug(f"got {len(reservations)} reservations")
        return render_template(
            "reservation/partial/reservation.html", reservations=reservations, restaurant=restaurant
        )
    except Exception as e:
        LOG.error(f"could not delete reservation '{e}'")

