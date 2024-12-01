import datetime
from unittest import mock

from ..infrastructure.config import Config
from ..store.menu_repository import MenuRepository
from ..store.repository_test_helpers import create_restaurant_data
from ..store.restaurant_repository import RestaurantRepository
from ..store.table_repository import TableRepository
from .service import RestaurantService


def test_restaurant_open():
    restaurant_repo_mock = mock.Mock(spec=RestaurantRepository)
    restaurant_repo_mock.get_restaurant_by_id.return_value = create_restaurant_data()
    menu_repo_mock = mock.Mock(spec=MenuRepository)
    table_repo_mock = mock.Mock(spec=TableRepository)
    # load the configuration to be able to access the settings as class attributes
    _ = Config().load_from_data({"SECRET_KEY": "very-secret"})

    svc = RestaurantService(restaurant_repo_mock, menu_repo_mock, table_repo_mock)
    # the date 2024-09-16 is a Monday
    assert svc.is_restaurant_open(1, datetime.date(2024, 9, 16), datetime.time(12, 0, 0), datetime.time(14, 0, 0))
    # too early
    assert not svc.is_restaurant_open(1, datetime.date(2024, 9, 16), datetime.time(9, 0, 0), datetime.time(14, 0, 0))
    # too late
    assert not svc.is_restaurant_open(1, datetime.date(2024, 9, 16), datetime.time(11, 0, 0), datetime.time(22, 30, 0))
    # exact
    assert svc.is_restaurant_open(1, datetime.date(2024, 9, 16), datetime.time(10, 0, 0), datetime.time(22, 0, 0))
    # exact: the date 2024-09-17 is a Tuesday
    assert svc.is_restaurant_open(1, datetime.date(2024, 9, 17), datetime.time(10, 0, 0), datetime.time(22, 0, 0))
    # wrong weekday: the date 2024-09-18 is a Wednesday
    assert not svc.is_restaurant_open(1, datetime.date(2024, 9, 18), datetime.time(10, 0, 0), datetime.time(22, 0, 0))
