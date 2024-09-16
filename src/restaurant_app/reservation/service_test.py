import datetime
from unittest import mock

from ..restaurant.service import RestaurantService
from ..store.entities import ReservationEntity, TableEntity
from ..store.reservation_repo import ReservationRepository
from ..store.table_repository import TableRepository
from .models import ReservationRequestModel
from .service import ReservationService


def test_reservation_table():
    restaurant_svc_mock = mock.Mock(spec=RestaurantService)
    restaurant_svc_mock.is_restaurant_open.return_value = True

    reservation_repo_mock = mock.Mock(spec=ReservationRepository)
    reservation_repo_mock.get_table_reservations_for_date.return_value = [
        ReservationEntity(
            reservation_date=datetime.date(2024, 9, 16),
            time_from=datetime.time(18, 0, 0),
            time_until=datetime.time(19, 0, 0),
            people=3,
            reservation_name="Test1",
            reservation_number="1",
        ),
        ReservationEntity(
            reservation_date=datetime.date(2024, 9, 16),
            time_from=datetime.time(20, 30, 0),
            time_until=datetime.time(22, 0, 0),
            people=3,
            reservation_name="Test2",
            reservation_number="2",
        ),
    ]

    table_repo_mock = mock.Mock(spec=TableRepository)
    table_repo_mock.get_tables_with_capacity.return_value = [
        TableEntity(id=1, table_number="1", seats=4, restaurant_id=1)
    ]

    reservation_svc = ReservationService(
        restaurant_svc=restaurant_svc_mock, reservation_repo=reservation_repo_mock, table_repo=table_repo_mock
    )

    reservation_svc.reserve(
        ReservationRequestModel(
            restaurant_id=1,
            name="Test",
            num_people=4,
            time_from=datetime.time(19, 0, 0),
            time_until=datetime.time(20, 30, 0),
            reservation_date=datetime.date(2024, 9, 16),
        )
    )
