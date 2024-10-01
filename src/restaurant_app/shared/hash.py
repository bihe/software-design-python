import hashlib

from flask import request

from ..infrastructure.config import Config
from .errors import BadRequestHashError


def get_hash_value(value: str) -> str:
    salt = Config.SECRET_KEY  # re-use the defined flask-secret-key for hashing
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
