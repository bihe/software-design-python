from datetime import time
from typing import List

from ..store.entities import AddressEntity, MenuEntity, RestaurantEntity, TableEntity
from ..store.menu_repository import MenuRepository
from ..store.restaurant_repository import RestaurantRepository
from ..store.table_repository import TableRepository
from .models import AddressModel, MenuModel, RestaurantModel, TableModel, WeekDay


class NotFoundError(Exception):
    """An entry cannot be found error"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


_LIST_DELIMINATOR = ";"


def _mapDayFromEnum(days: List[WeekDay]) -> str:
    db_days: List[str] = []
    for day in days:
        db_days.append(str(day))
    return _LIST_DELIMINATOR.join(db_days)


def _mapDayToEnum(openDays: str) -> List[WeekDay]:
    days: List[WeekDay] = []
    for day in openDays.split(_LIST_DELIMINATOR):
        match day:
            case "MONDAY":
                days.append(WeekDay.MONDAY)
            case "TUESDAY":
                days.append(WeekDay.TUESDAY)
            case "WEDNESDAY":
                days.append(WeekDay.WEDNESDAY)
            case "THURSDAY":
                days.append(WeekDay.THURSDAY)
            case "FRIDAY":
                days.append(WeekDay.FRIDAY)
            case "SATURDAY":
                days.append(WeekDay.SATURDAY)
            case "SUNDAY":
                days.append(WeekDay.SUNDAY)
    return days


# TODO: for service tests - mock repositories
# https://python-dependency-injector.ets-labs.org/examples/fastapi-sqlalchemy.html


def _mapEntityToModel(res: RestaurantEntity) -> RestaurantModel:
    open_days = _mapDayToEnum(res.open_days)

    def _mapTimeToHours(t: time) -> List[int]:
        times: List[int] = []
        times.append(t.hour)
        times.append(t.minute)
        return times

    restaurant_model = RestaurantModel(
        id=res.id,
        address=AddressModel(
            street=res.address.street,
            zip=res.address.zip,
            city=res.address.city,
            countryCode=res.address.country,
        ),
        menus=None,
        tables=None,
        name=res.name,
        openFrom=_mapTimeToHours(res.open_from),
        openUntil=_mapTimeToHours(res.open_until),
        openDays=open_days,
    )

    # map to MenuModel
    if res.menus is not None:
        menus: List[MenuModel] = []
        for menu in res.menus:
            menu_model = MenuModel(id=menu.id, name=menu.name, price=menu.price, category=menu.category)
            menus.append(menu_model)
        restaurant_model.menus = menus

    # map to TableModel
    if res.tables is not None:
        tables: List[TableModel] = []
        for table in res.tables:
            table_model = TableModel(id=table.id, number=table.table_number, places=table.seats)
            tables.append(table_model)
        restaurant_model.tables = tables

    return restaurant_model


class RestaurantService:
    def __init__(self, repo: RestaurantRepository):
        self._repo = repo

    def __str__(self) -> str:
        return "RestaurantService"

    def get_all(self) -> List[RestaurantModel]:
        restaurants: List[RestaurantModel] = []
        res = self._repo.get_all_restaurants()
        if res is not None:
            for r in res:
                restaurants.append(_mapEntityToModel(r))
        return restaurants

    def save(self, restaurant: RestaurantModel) -> RestaurantModel:

        def work_in_transaction(session) -> List[RestaurantModel]:
            res_repo = RestaurantRepository.create_with_session(session)
            menu_repo = MenuRepository.create_with_session(session)
            table_repo = TableRepository.create_with_session(session)

            # lookup the address first
            a = restaurant.address
            find_addr = AddressEntity()
            find_addr.city = a.city
            find_addr.street = a.street
            find_addr.zip = a.zip
            find_addr.country = a.countryCode

            addr = res_repo.find_address(find_addr)
            if addr is None:
                # nothing found, use the provided address
                a = restaurant.address
                addr = AddressEntity()
                addr.city = a.city
                addr.street = a.street
                addr.zip = a.zip
                addr.country = a.countryCode

            # determine if this is a new entry or if the restaurant-entry exists
            store_restaurant = RestaurantEntity()
            res_id = restaurant.id or 0
            if res_id > 0:
                store_restaurant = res_repo.get_restaurant_by_id(restaurant.id)
                if store_restaurant is None:
                    raise NotFoundError(f"a restaurant with id '{restaurant.id}' is not available")
            else:
                # check if this is an existing restaurant
                store_restaurant = (
                    res_repo.find_restaurants_by_name_and_address(restaurant.name, addr) or RestaurantEntity()
                )

            # set the values of the restaurant with the provided values
            store_restaurant.name = restaurant.name
            store_restaurant.open_from = time(restaurant.openFrom[0], restaurant.openFrom[1], 0)
            store_restaurant.open_until = time(restaurant.openUntil[0], restaurant.openUntil[1], 0)
            store_restaurant.open_days = _mapDayFromEnum(restaurant.openDays)
            store_restaurant.address = addr

            saved = res_repo.save(store_restaurant)

            # process the menu entries
            if restaurant.menus is not None:
                for menu in restaurant.menus:
                    menu_repo.save(
                        MenuEntity(name=menu.name, price=menu.price, category=menu.category, restaurant=saved)
                    )

            # process the tables
            if restaurant.tables is not None:
                for table in restaurant.tables:
                    table_repo.save(TableEntity(table_number=table.number, seats=table.places, restaurant=saved))

            result: List[RestaurantModel] = []
            result.append(_mapEntityToModel(saved))
            return result

        result = self._repo.unit_of_work(work_in_transaction)
        if result is None or len(result) == 0:
            return None
        return result[0]
