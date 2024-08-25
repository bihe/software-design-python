from contextlib import AbstractContextManager
from typing import Callable, List

from sqlalchemy.orm import Session

from .models import RestaurantModel


class RestaurantRepository:

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        pass

    def get_all_restaurants(self) -> List[RestaurantModel]:
        with self.session_factory() as session:
            restaurantes = session.query(RestaurantModel).all()
            return restaurantes

    def save(self, restaurant: RestaurantModel) -> RestaurantModel:
        with self.session_factory() as session:
            if restaurant.id is not None and restaurant.id > 0:
                existing = session.get(RestaurantModel, restaurant.id)
                if existing is not None:
                    existing.name = restaurant.name
                    existing.open_from = restaurant.open_from
                    existing.open_until = restaurant.open_until
                    session.add(existing)
                    session.commit()
                    return existing

            # new or not found
            if restaurant.address.id is None:
                session.add(restaurant.address)
            session.add(restaurant)
            session.commit()
            return restaurant
