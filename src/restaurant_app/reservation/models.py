from dataclasses import dataclass
from datetime import datetime, time

from ..restaurant.models import TableModel


@dataclass
class ReservationRequestModel:
    restaurant_id: int
    name: str
    num_people: int
    time_from: time.Time
    time_until: time.Time
    reservation_date: datetime.Date


@dataclass
class ReservationModel:
    id: int
    number: str
    name: str
    num_people: int
    time_from: time.Time
    time_until: time.Time
    reservation_date: datetime.Date
    reserved_table: TableModel
