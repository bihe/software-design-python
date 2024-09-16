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
