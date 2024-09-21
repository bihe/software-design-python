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

    def displayOpenTime(self) -> str:
        return f"{self.openFrom[0]:02}:{self.openFrom[1]:02} - {self.openUntil[0]:02}:{self.openUntil[1]:02}"

    def tableCount(self) -> int:
        if self.tables is None:
            return 0
        return len(self.tables)
