import datetime
from ast import List

from dependency_injector.wiring import Provide, inject
from flask import Blueprint, redirect, render_template, request, url_for

from ..auth.views import login_required
from ..infrastructure.cache import Cache
from ..infrastructure.container import Container
from ..infrastructure.logger import LOG
from ..shared.view_helpers import NotFoundError, get_hash_value, prepare_view_model, valid_hash, valid_hash_supplied
from .forms import RestaurantForm
from .models import AddressModel, RestaurantModel, WeekDay
from .service import RestaurantService

bp = Blueprint("restaurant", __name__)


@bp.get("/restaurants")
@login_required
@inject
def index(
    restaurant_svc: RestaurantService = Provide[Container.restaurant_svc], cache: Cache = Provide[Container.cache]
):
    LOG.info("view restaurant/index")
    restaurants = restaurant_svc.get_all()
    LOG.debug(f"get {len(restaurants)} restaurants")
    for r in restaurants:
        r.id_hash = get_hash_value(str(r.id))
    model_params = prepare_view_model(cache, restaurants=restaurants)
    return render_template("restaurant/index.html", **model_params)


def get_time(item: List) -> datetime.time:
    return datetime.time(item[0], item[1], 0)


@bp.route("/restaurant/<restaurant_id>", methods=["GET", "POST"])
@login_required
@inject
def restaurant(
    restaurant_id: int,
    restaurant_svc: RestaurantService = Provide[Container.restaurant_svc],
    cache: Cache = Provide[Container.cache],
):
    form: RestaurantForm = None

    if request.method == "GET":
        LOG.info(f"display the restaurant details for id '{restaurant_id}'")
        valid_hash(str(restaurant_id))
        restaurant = restaurant_svc.get_by_id(restaurant_id)
        if restaurant is None:
            raise NotFoundError(f"cannot find restaurant by id '{restaurant_id}'")
        form = RestaurantForm(
            data={
                "id": restaurant.id,
                "h": get_hash_value(str(restaurant.id)),
                "name": restaurant.name,
                "street": restaurant.address.street,
                "city": restaurant.address.city,
                "zip": restaurant.address.zip,
                "country": restaurant.address.country_code,
                "open_from": get_time(restaurant.open_from),
                "open_until": get_time(restaurant.open_until),
                "open_monday": True if (WeekDay.MONDAY in restaurant.open_days) else False,
                "open_tuesday": True if (WeekDay.TUESDAY in restaurant.open_days) else False,
                "open_wednesday": True if (WeekDay.WEDNESDAY in restaurant.open_days) else False,
                "open_thursday": True if (WeekDay.THURSDAY in restaurant.open_days) else False,
                "open_friday": True if (WeekDay.FRIDAY in restaurant.open_days) else False,
                "open_saturday": True if (WeekDay.SATURDAY in restaurant.open_days) else False,
                "open_sunday": True if (WeekDay.SUNDAY in restaurant.open_days) else False,
            }
        )

    elif request.method == "POST":
        form = RestaurantForm(request.form)
        if form.validate():
            valid_hash_supplied(restaurant_id, request.form["h"])
            open_days: List[WeekDay] = []
            if form.open_monday.data:
                open_days.append(WeekDay.MONDAY)
            if form.open_tuesday.data:
                open_days.append(WeekDay.TUESDAY)
            if form.open_wednesday.data:
                open_days.append(WeekDay.WEDNESDAY)
            if form.open_thursday.data:
                open_days.append(WeekDay.THURSDAY)
            if form.open_friday.data:
                open_days.append(WeekDay.FRIDAY)
            if form.open_saturday.data:
                open_days.append(WeekDay.SATURDAY)
            if form.open_sunday.data:
                open_days.append(WeekDay.SUNDAY)
            restaurant = RestaurantModel(
                id=int(form.id.data),
                name=form.name.data,
                open_from=[form.open_from.data.hour, form.open_from.data.minute],
                open_until=[form.open_until.data.hour, form.open_until.data.minute],
                address=AddressModel(
                    street=form.street.data, city=form.city.data, zip=form.zip.data, country_code=form.country.data
                ),
                open_days=open_days,
                tables=None,
                menus=None,
            )
            restaurant_svc.save(restaurant)
            return redirect(url_for("restaurant.index"))

    model_params = prepare_view_model(cache, form=form)
    return render_template("restaurant/detail.html", **model_params)
