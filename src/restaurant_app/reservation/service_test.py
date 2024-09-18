import datetime
from typing import List
from unittest import mock

import pytest

from ..restaurant.service import RestaurantService
from ..store.entities import ReservationEntity, TableEntity
from ..store.reservation_repo import ReservationRepository
from ..store.table_repository import TableRepository
from .models import ReservationRequestModel
from .service import ReservationError, ReservationService


def test_reservation_table():

    reservation_repo = ReservationRepository(None, None)

    def mocked_reservations() -> List[ReservationEntity]:
        return [
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
                time_from=datetime.time(20, 00, 0),
                time_until=datetime.time(22, 0, 0),
                people=3,
                reservation_name="Test2",
                reservation_number="2",
            ),
        ]

    def mocked_save(entity: ReservationEntity) -> ReservationEntity:
        entity.id = 1
        return entity

    # this is heavy-duty patching of the reservation_repo
    # we mangle the methods used in the service to behave in a way as we want it
    # either simply by defining the return_value (= easy)
    # or by utilizing the option of side_effect, where we can even access the supplied arguments
    with (
        mock.patch.object(reservation_repo, "get_table_reservations_for_date", return_value=mocked_reservations()),
        # side-effect: the suplied argument is a Callable -> call it!
        mock.patch.object(reservation_repo, "unit_of_work", side_effect=lambda func: func(None)),
        mock.patch.object(reservation_repo, "new_session", return_value=reservation_repo),
        mock.patch.object(reservation_repo, "is_reservation_number_in_use", return_value=False),
        # use the method above to change the supplied value of the save-method
        mock.patch.object(reservation_repo, "save", side_effect=mocked_save),
    ):
        # in this case we ask to crate a MagicMock based on the "template" of the supplied class (=spec)
        restaurant_svc_mock = mock.Mock(spec=RestaurantService)
        restaurant_svc_mock.is_restaurant_open.return_value = True
        # again: mock based on spec
        table_repo_mock = mock.Mock(spec=TableRepository)
        table_repo_mock.get_tables_with_capacity.return_value = [
            TableEntity(id=1, table_number="1", seats=4, restaurant_id=1)
        ]

        # provide the patched object and two created mocks
        reservation_svc = ReservationService(
            restaurant_svc=restaurant_svc_mock, reservation_repo=reservation_repo, table_repo=table_repo_mock
        )

        # a slot before the 20:00-22:00 reservation
        reservation = reservation_svc.reserve(
            ReservationRequestModel(
                restaurant_id=1,
                name="Test",
                num_people=4,
                time_from=datetime.time(19, 0, 0),
                time_until=datetime.time(20, 00, 0),
                reservation_date=datetime.date(2024, 9, 16),
            )
        )

        assert reservation.id > 0
        assert reservation.number != ""  # as this number is random, we cannot compare it to a real value
        assert len(reservation.number) == 7  # but we know the lenght
        assert reservation.reserved_table is not None  # we got a table
        assert reservation.reserved_table.id == 1
        assert reservation.reserved_table.number == "1"
        assert reservation.reserved_table.places >= 4

        # a slot after the 20:00-22:00 reservation
        reservation = reservation_svc.reserve(
            ReservationRequestModel(
                restaurant_id=1,
                name="Test",
                num_people=4,
                time_from=datetime.time(22, 0, 0),
                time_until=datetime.time(23, 00, 0),
                reservation_date=datetime.date(2024, 9, 16),
            )
        )

        assert reservation.id > 0
        assert reservation.number != ""  # as this number is random, we cannot compare it to a real value
        assert len(reservation.number) == 7  # but we know the lenght
        assert reservation.reserved_table is not None  # we got a table
        assert reservation.reserved_table.id == 1
        assert reservation.reserved_table.number == "1"
        assert reservation.reserved_table.places >= 4

        # if there is no table available, we get an error
        with pytest.raises(ReservationError):
            reservation_svc.reserve(
                ReservationRequestModel(
                    restaurant_id=1,
                    name="Test",
                    num_people=4,
                    time_from=datetime.time(20, 0, 0),  # the request overlaps with an existing reservation
                    time_until=datetime.time(22, 0, 0),
                    reservation_date=datetime.date(2024, 9, 16),
                )
            )

        with pytest.raises(ReservationError):
            reservation_svc.reserve(
                ReservationRequestModel(
                    restaurant_id=1,
                    name="Test",
                    num_people=4,
                    time_from=datetime.time(20, 0, 0),  # the request overlaps with an existing reservation
                    time_until=datetime.time(21, 0, 0),
                    reservation_date=datetime.date(2024, 9, 16),
                )
            )

        with pytest.raises(ReservationError):
            reservation_svc.reserve(
                ReservationRequestModel(
                    restaurant_id=1,
                    name="Test",
                    num_people=4,
                    time_from=datetime.time(21, 0, 0),  # the request overlaps with an existing reservation
                    time_until=datetime.time(22, 0, 0),
                    reservation_date=datetime.date(2024, 9, 16),
                )
            )

        with pytest.raises(ReservationError):
            reservation_svc.reserve(
                ReservationRequestModel(
                    restaurant_id=1,
                    name="Test",
                    num_people=4,
                    time_from=datetime.time(19, 0, 0),  # the request overlaps with an existing reservation
                    time_until=datetime.time(21, 0, 0),
                    reservation_date=datetime.date(2024, 9, 16),
                )
            )

        with pytest.raises(ReservationError):
            reservation_svc.reserve(
                ReservationRequestModel(
                    restaurant_id=1,
                    name="Test",
                    num_people=4,
                    time_from=datetime.time(21, 0, 0),  # the request overlaps with an existing reservation
                    time_until=datetime.time(23, 0, 0),
                    reservation_date=datetime.date(2024, 9, 16),
                )
            )
