import calendar
import datetime
from datetime import time
from typing import List

from ..shared.errors import NotFoundError
from ..store.entities import AddressEntity, MenuEntity, RestaurantEntity, TableEntity
from ..store.menu_repository import MenuRepository
from ..store.restaurant_repository import RestaurantRepository
from ..store.table_repository import TableRepository
from .models import RestaurantModel
from .service_model_mapper import mapDayFromEnum, mapEntityToModel


class RestaurantService:
    def __init__(self, restaurant_repo: RestaurantRepository, menu_repo: MenuRepository, table_repo: TableRepository):
        self._restaurant_repo = restaurant_repo
        self._menu_repo = menu_repo
        self._table_repo = table_repo

    def __str__(self) -> str:
        return "RestaurantService"

    def get_all(self) -> List[RestaurantModel]:
        restaurants: List[RestaurantModel] = []
        res = self._restaurant_repo.get_all_restaurants()
        if res is not None:
            for r in res:
                restaurants.append(mapEntityToModel(r))
        return restaurants

    def get_by_id(self, id: int) -> RestaurantModel:
        res = self._restaurant_repo.get_restaurant_by_id(id)
        if res is None:
            return None
        return mapEntityToModel(res)

    def is_restaurant_open(
        self, restaurant_id: int, date: datetime.date, time_from: datetime.time, time_until: datetime.time
    ) -> bool:
        restaurant = self._restaurant_repo.get_restaurant_by_id(restaurant_id)
        if restaurant is None:
            raise NotFoundError(f"a restaurant with id '{restaurant.id}' is not available")

        restaurant_model = mapEntityToModel(restaurant)

        # 1) get the weekday of the date to determine if the restaurant is open
        open_on_date = False
        weekday_name = calendar.day_name[date.weekday()]
        for day in restaurant_model.open_days:
            if str(day) == weekday_name.upper():
                open_on_date = True
                break
        if not open_on_date:
            return False

        # 2) check if the given time is within the opening hours of the restaurant
        open_from = datetime.time(restaurant_model.open_from[0], restaurant_model.open_from[1])
        open_until = datetime.time(restaurant_model.open_until[0], restaurant_model.open_until[1])

        if time_from >= open_from and time_until <= open_until:
            return True

        return False

    def save(self, restaurant: RestaurantModel) -> RestaurantModel:

        def work_in_transaction(session) -> List[RestaurantModel]:
            res_repo = self._restaurant_repo.new_session(session)
            menu_repo = self._menu_repo.new_session(session)
            table_repo = self._table_repo.new_session(session)

            # lookup the address first
            a = restaurant.address
            find_addr = AddressEntity()
            find_addr.city = a.city
            find_addr.street = a.street
            find_addr.zip = a.zip
            find_addr.country = a.country_code

            addr = res_repo.find_address(find_addr)
            if addr is None:
                # nothing found, use the provided address
                a = restaurant.address
                addr = AddressEntity()
                addr.city = a.city
                addr.street = a.street
                addr.zip = a.zip
                addr.country = a.country_code

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
            store_restaurant.open_from = time(restaurant.open_from[0], restaurant.open_from[1], 0)
            store_restaurant.open_until = time(restaurant.open_until[0], restaurant.open_until[1], 0)
            store_restaurant.open_days = mapDayFromEnum(restaurant.open_days)
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

        result = self._restaurant_repo.unit_of_work(work_in_transaction)
        if result is None or len(result) == 0:
            return None
        return result[0]
