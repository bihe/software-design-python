import time

from dependency_injector.wiring import Provide, inject
from flask import Blueprint, render_template, request
from pydantic import BaseModel, ValidationError, model_validator

from ..auth.views import login_required
from ..infrastructure.cache import Cache
from ..infrastructure.container import Container
from ..infrastructure.logger import LOG
from ..shared.view_helpers import NotFoundError, get_hash_value, prepare_view_model, valid_hash, valid_hash_supplied
from .models import AddressModel, RestaurantModel
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


@bp.get("/restaurant/<restaurant_id>")
@login_required
@inject
def detail(
    restaurant_id: int,
    restaurant_svc: RestaurantService = Provide[Container.restaurant_svc],
    cache: Cache = Provide[Container.cache],
):
    LOG.info("view restaurant/detail")
    valid_hash(str(restaurant_id))
    restaurant = restaurant_svc.get_by_id(restaurant_id)
    if restaurant is None:
        raise NotFoundError(f"cannot find restaurant by id '{restaurant_id}'")
    restaurant.id_hash = get_hash_value(str(restaurant.id))
    model_params = prepare_view_model(cache, restaurant=restaurant)
    return render_template("restaurant/detail.html", **model_params)


class RestaurantViewModel(BaseModel):
    name: str
    street: str
    zip: str
    city: str
    country: str
    open_from: str
    open_until: str

    @model_validator(mode="after")
    def validate_open_times(self):
        time_open_from = time.strptime(self.open_from, "%H:%M")
        time_open_until = time.strptime(self.open_until, "%H:%M")
        if time_open_until < time_open_from:
            raise ValueError("open_until canot be before open_from")
        return self


@bp.post("/restaurant/<restaurant_id>")
@login_required
@inject
def save(
    restaurant_id: int,
    restaurant_svc: RestaurantService = Provide[Container.restaurant_svc],
    cache: Cache = Provide[Container.cache],
):
    LOG.info("view restaurant/save")
    valid_hash_supplied(restaurant_id, request.form["h"])

    try:
        view_model = RestaurantViewModel(
            name=request.form["name"],
            street=request.form["address.street"],
            zip=request.form["address.zip"],
            city=request.form["address.city"],
            country=request.form["address.country"],
            open_from=request.form["open_from"],
            open_until=request.form["open_until"],
        )
    except ValidationError as e:
        LOG.debug(f"got validaton error: {e}")
        time_open_from = time.strptime(request.form["open_from"], "%H:%M")
        time_open_until = time.strptime(request.form["open_until"], "%H:%M")
        restaurant = RestaurantModel(
            id=restaurant_id,
            id_hash=request.form["h"],
            name=request.form["name"],
            address=AddressModel(
                city=request.form["address.city"],
                zip=request.form["address.city"],
                street=request.form["address.street"],
                country_code=request.form["address.country"],
            ),
            open_from=[time_open_from.tm_hour, time_open_from.tm_min],
            open_until=[time_open_until.tm_hour, time_open_until.tm_min],
            tables=[],
            menus=[],
            open_days=[],
        )

        model_params = prepare_view_model(cache, restaurant=restaurant)
        model_params["errors"] = e.errors()
        return render_template("restaurant/detail.html", **model_params)

    return str(view_model)
