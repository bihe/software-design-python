from ..restaurant.models import TableModel
from ..store.entities import ReservationEntity
from .models import ReservationModel


def mapEntityToModel(res: ReservationEntity) -> ReservationModel:
    return ReservationModel(
        id=res.id,
        number=res.reservation_number,
        name=res.reservation_name,
        num_people=res.people,
        time_from=res.time_from,
        time_until=res.time_until,
        reservation_date=res.reservation_date,
        reserved_table=TableModel(id=res.tables[0].id, number=res.tables[0].table_number, places=res.tables[0].seats),
    )
