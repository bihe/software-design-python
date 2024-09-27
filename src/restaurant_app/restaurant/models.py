import enum
from dataclasses import dataclass
from typing import List


@dataclass
class AddressModel:
    street: str
    city: str
    zip: str
    country_code: str


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
    open_days: List[WeekDay]
    open_from: List[int]
    open_until: List[int]
    address: AddressModel
    tables: List[TableModel]
    menus: List[MenuModel]

    def open_from_format(self) -> str:
        return f"{self.open_from[0]:02}:{self.open_from[1]:02}"

    def open_until_format(self) -> str:
        return f"{self.open_until[0]:02}:{self.open_until[1]:02}"

    def display_open_time(self) -> str:
        return f"{self.open_from[0]:02}:{self.open_from[1]:02} - {self.open_until[0]:02}:{self.open_until[1]:02}"

    def table_count(self) -> int:
        if self.tables is None:
            return 0
        return len(self.tables)
