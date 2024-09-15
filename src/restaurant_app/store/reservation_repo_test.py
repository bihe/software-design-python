import datetime
from typing import Any, List

from .entities import ReservationEntity
from .repository_test_helpers import get_database
from .reservation_repo import ReservationRepository


def test_reservation_repository_crud():

    def action(session) -> List[Any]:
        reservation_repo = ReservationRepository.create_with_session(session)
        res = reservation_repo.save(
            ReservationEntity(
                reservation_date=datetime.datetime.now(),
                time_from=datetime.time(20, 0, 0),
                time_until=datetime.time(22, 0, 0),
                people=4,
                reservation_name="Test",
                reservation_number="1234",
            )
        )
        reservation_repo.sync()
        assert res.id > 0
        assert res.reservation_name == "Test"
        assert res.reservation_number == "1234"

        # update the entry
        res.reservation_name = "Test_update"
        res.time_until = datetime.time(23, 0, 0)
        res.people = 3
        update = reservation_repo.save(res)

        assert update.reservation_name == "Test_update"
        assert update.time_until == datetime.time(23, 0, 0)
        assert update.people == 3

        result = []
        result.append(update.id)
        return result

    repo = ReservationRepository(get_database().managed_session)
    res_id = repo.unit_of_work(action)
    print(res_id)
    find = repo.get_reservation_by_id(res_id)
    assert find is not None
    assert find.reservation_name == "Test_update"
    assert find.time_until == datetime.time(23, 0, 0)

    find = repo.get_reservation_by_number("1234")
    assert find is not None
    assert find.reservation_name == "Test_update"
    assert find.time_until == datetime.time(23, 0, 0)

    assert repo.is_reservation_number_in_use("1234")
    assert not repo.is_reservation_number_in_use("2345")
