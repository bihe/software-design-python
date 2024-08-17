from typing import List

from ...store.models import RestaurantModel
from ...store.restaurant_repository import RestaurantRepository


class RestaurantService:
    def __init__(self, repo: RestaurantRepository):
        self._repo = repo

    def get_service_name(self) -> str:
        restaurants: List[RestaurantModel] = self._repo.get_all_restaurants()
        if len(restaurants) == 0:
            return "restaurant-service without restaurants in db"
        return f"we have {len(restaurants)} restaurant(s) availabel in the db"
