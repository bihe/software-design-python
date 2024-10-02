import datetime
from dataclasses import dataclass

from ..restaurant.models import TableModel


@dataclass
class ReservationRequestModel:
    restaurant_id: int
    name: str
    num_people: int
    time_from: datetime.time
    time_until: datetime.time
    reservation_date: datetime.date


@dataclass
class ReservationModel:
    id: int
    number: str
    name: str
    num_people: int
    time_from: datetime.time
    time_until: datetime.time
    reservation_date: datetime.date
    reserved_table: TableModel

    def date_format(self) -> str:
        return self.reservation_date.strftime("%Y-%m-%d")

    def reservation_time_format(self) -> str:
        return f"{self.time_from.strftime("%H:%M")} - {self.time_until.strftime("%H:%M")}"
