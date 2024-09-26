import hashlib
from typing import Any, Dict

from flask import current_app, request, session

from ..auth.models import User
from ..infrastructure.cache import Cache

user_key_format = "user_"
session_user_id = "user_id"


class UserCacheMissError(Exception):
    """
    UserCacheMissError indicates that the needed value from the cache is not availabe.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class BadRequestHashError(Exception):
    """
    BadRequestHashError indicates, that the supplied hash value is not correct.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class NotFoundError(Exception):
    """
    NotFoundError indicates, that a requested object is not available
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


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


def get_hash_value(value: str) -> str:
    salt = current_app.config["SECRET_KEY"]  # re-use the defined flask-secret-key for hashing
    return hashlib.sha256(salt.encode() + value.encode()).hexdigest()


def valid_hash(value: str):
    supplied_hash = request.args.get("h", "")
    hash_value = get_hash_value(value)
    if hash_value != supplied_hash:
        raise BadRequestHashError("the value does not match the supplied hash")


def valid_hash_supplied(value: str, supplied_hash: str):
    hash_value = get_hash_value(value)
    if hash_value != supplied_hash:
        raise BadRequestHashError("the value does not match the supplied hash")
