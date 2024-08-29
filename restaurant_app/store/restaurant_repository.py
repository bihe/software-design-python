from contextlib import AbstractContextManager
from typing import Callable, List, Self

from sqlalchemy.orm import Session

from .base_repository import BaseRepository
from .models import RestaurantModel


class RestaurantRepository(BaseRepository):

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]], session: Session = None):
        super().__init__(session_factory=session_factory, session=session)

    @classmethod
    def create_with_session(cls, session: Session) -> Self:
        return RestaurantRepository(session_factory=None, session=session)

    def get_all_restaurants(self) -> List[RestaurantModel]:
        session = self.get_session()
        restaurantes = session.query(RestaurantModel).all()
        return restaurantes

    def save(self, restaurant: RestaurantModel) -> RestaurantModel:
        session = self.get_session()
        if restaurant.id is not None and restaurant.id > 0:
            existing = session.get(RestaurantModel, restaurant.id)
            if existing is not None:
                existing.name = restaurant.name
                existing.open_from = restaurant.open_from
                existing.open_until = restaurant.open_until
                session.add(existing)
                return existing

        # new or not found
        if restaurant.address.id is None:
            session.add(restaurant.address)
        session.add(restaurant)
        return restaurant
