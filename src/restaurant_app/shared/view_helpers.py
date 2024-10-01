from typing import Any, Dict, List

from flask import session

from ..auth.models import User
from ..infrastructure.cache import Cache
from ..restaurant.models import RestaurantModel
from .errors import UserCacheMissError

user_key_format = "user_"
session_user_id = "user_id"
restaurants_cache_key = "restaurants"


def get_user_id_from_session() -> str:
    if session_user_id in session:
        user_id = session[session_user_id]
        return user_id
    return None


def set_user_id_to_session(id: str):
    session[session_user_id] = id


def clear_session():
    session.clear()


def get_user_cache_key(user_id: str) -> str:
    return f"{user_key_format}{user_id}"


def get_user_from_cache(cache: Cache, user_id: str) -> User:
    return cache.get(get_user_cache_key(user_id))


def put_user_to_cache(cache: Cache, user: User):
    return cache.put(get_user_cache_key(user.id), user)


def delete_user_from_cache(cache: Cache, user_id: str):
    cache.delete(get_user_cache_key(user_id))


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
    user_id = get_user_id_from_session()
    if user_id is not None:
        # load the user-object from cache
        user = get_user_from_cache(cache, user_id)
        if user is None:
            raise UserCacheMissError("cannot get the user from the cache!")
        args["user"] = user
    return args
