from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session

from .models import RestaurantModel


class RestaurantRepository:

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        pass

    def get_all_restaurants(self):
        with self.session_factory() as session:
            restaurantes = session.query(RestaurantModel).all()
            return restaurantes

    def save(self, restaurant: RestaurantModel):
        with self.session_factory() as session:
            if restaurant.id > 0:
                existing = session.get(RestaurantModel, restaurant.id)
                if existing is not None:
                    existing.name = restaurant.name
                    session.add(existing)
                    session.commit()
                    return existing

            # new or not found
            new_restaurant = RestaurantModel(name=restaurant.name)
            session.add(new_restaurant)
            session.commit()
            return new_restaurant
