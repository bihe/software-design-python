import calendar
import datetime
from datetime import time
from typing import List

from ..store.entities import AddressEntity, MenuEntity, RestaurantEntity, TableEntity
from ..store.menu_repository import MenuRepository
from ..store.restaurant_repository import RestaurantRepository
from ..store.table_repository import TableRepository
from .models import RestaurantModel
from .service_model_mapper import mapDayFromEnum, mapEntityToModel


class NotFoundError(Exception):
    """An entry cannot be found error"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


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
                restaurants.append(mapEntityToModel(r))
        return restaurants

    def is_restaurant_open(
        self, restaurant_id: int, date: datetime.date, time_from: datetime.time, time_until: datetime.time
    ) -> bool:
        restaurant = self._repo.get_restaurant_by_id(restaurant_id)
        if restaurant is None:
            raise NotFoundError(f"a restaurant with id '{restaurant.id}' is not available")

        restaurant_model = mapEntityToModel(restaurant)

        # 1) get the weekday of the date to determine if the restaurant is open
        open_on_date = False
        weekday_name = calendar.day_name[date.weekday()]
        for day in restaurant_model.openDays:
            if str(day) == weekday_name.upper():
                open_on_date = True
                break
        if not open_on_date:
            return False

        # 2) check if the given time is within the opening hours of the restaurant
        open_from = datetime.time(restaurant_model.openFrom[0], restaurant_model.openFrom[1])
        open_until = datetime.time(restaurant_model.openUntil[0], restaurant_model.openUntil[1])

        if time_from >= open_from and time_until <= open_until:
            return True

        return False

    def save(self, restaurant: RestaurantModel) -> RestaurantModel:

        def work_in_transaction(session) -> List[RestaurantModel]:
            # TODO: change the static methods to instance methods
            # so that the repository created is defined by the injected repo!!!
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
            store_restaurant.open_days = mapDayFromEnum(restaurant.openDays)
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
            result.append(mapEntityToModel(saved))
            return result

        result = self._repo.unit_of_work(work_in_transaction)
        if result is None or len(result) == 0:
            return None
        return result[0]
