import json
from typing import Any, Dict, List

from flask import session

from ..auth.models import User
from ..infrastructure.cache import Cache
from ..restaurant.models import RestaurantModel
from .errors import UserCacheMissError

user_session_key = "_user"
restaurants_cache_key = "restaurants"


def get_user_from_session() -> User:
    if user_session_key in session:
        serialized_user = session[user_session_key]
        if serialized_user is None:
            return None
        user = json.loads(serialized_user)
        return user
    return None


def set_user_to_session(user: User):
    if user is None:
        return
    serialized_user = json.dumps(vars(user))
    session[user_session_key] = serialized_user


def clear_session():
    session.clear()


def get_restaurants_from_cache(cache: Cache) -> List[RestaurantModel]:
    return cache.get(restaurants_cache_key)


def put_restaurants_to_cache(cache: Cache, restaurants: List[RestaurantModel]):
    return cache.put(restaurants_cache_key, restaurants)


def delete_restaurants_from_cache(cache: Cache):
    cache.delete(restaurants_cache_key)


def prepare_view_model(cache: Cache, **kwargs) -> Dict[str, Any]:
    args = {}
    for key in kwargs.keys():
        args[key] = kwargs[key]

    # retrieve the user-id from the session
    user = get_user_from_session()
    if user is not None:
        args["user"] = user
    else:
        raise UserCacheMissError("cannot get the user from the cache!")
    return args
