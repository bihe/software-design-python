from datetime import time

from .database import Database
from .models import AddressModel, RestaurantModel
from .restaurant_repository import RestaurantRepository


def test_restaurant_repository_crud():
    db = Database("sqlite://", False)
    db.create_database()
    repo = RestaurantRepository(db.session)

    addr = AddressModel()
    addr.city = "Salzburg"
    addr.country = "AT"
    addr.street = "Hauptstraße 1"
    addr.zip = 5020

    res = RestaurantModel()
    res.name = "Test-Restaurant"
    res.open_from = time(10, 0, 0)
    res.open_until = time(22, 0, 0)
    res.address = addr
    repo.save(res)
    # assert saved_res.id > 0

    all_restaurants = repo.get_all_restaurants()
    assert len(all_restaurants) == 1
