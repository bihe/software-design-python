import enum
from dataclasses import dataclass
from typing import List


@dataclass
class AddressModel:
    street: str
    city: str
    zip: str
    countryCode: str


@dataclass
class TableModel:
    id: int
    number: str
    places: int


@dataclass
class MenuModel:
    id: int
    name: str
    price: float
    category: str


class WeekDay(enum.StrEnum):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"


@dataclass
class RestaurantModel:
    id: int
    name: str
    openDays: List[WeekDay]
    openFrom: List[int]
    openUntil: List[int]
    address: AddressModel
    tables: List[TableModel]
    menus: List[MenuModel]
