from datetime import time
from typing import List

from ..store.restaurant_repository import RestaurantRepository
from .models import AddressModel, RestaurantModel, WeekDay


class NotFoundError(Exception):
    """An entry cannot be found error"""

    def __init__(self, salary, message):
        self.salary = salary
        self.message = message
        super().__init__(self.message)


_LIST_DELIMINATOR = ";"


class RestaurantService:
    def __init__(self, repo: RestaurantRepository):
        self._repo = repo

    def _mapDaysEnum(self, days: List[WeekDay]) -> str:
        db_days: List[str] = []
        for day in days:
            db_days.append(str(day))
        return _LIST_DELIMINATOR.join(db_days)

    def save(self, restaurant: RestaurantModel):
        # lookup the address first
        addr = self._repo.find_address(restaurant.address)
        if addr is None:
            # nothing found, use the provided address
            a = restaurant.address
            addr = AddressModel()
            addr.city = a.city
            addr.street = a.street
            addr.zip = a.zip
            addr.countryCode = a.countryCode

        # determine if this is a new entry or if the restaurant-entry exists
        store_restaurant = RestaurantModel()
        if restaurant.id is not None:
            store_restaurant = self._repo.get_restaurant_by_id(restaurant.id)
            if store_restaurant is None:
                raise NotFoundError(f"a restaurant with id '{restaurant.id}' is not available")

        # set the values of the restaurant with the provided values
        store_restaurant.name = restaurant.name
        store_restaurant.open_from = time(restaurant.openFrom[0], restaurant.openFrom[1], 0)
        store_restaurant.open_until = time(restaurant.openUntil[0], restaurant.openUntil[1], 0)
        store_restaurant.open_days = self._mapDaysEnum(restaurant.openDays)
        store_restaurant.address = addr

        self._repo.save(store_restaurant)
