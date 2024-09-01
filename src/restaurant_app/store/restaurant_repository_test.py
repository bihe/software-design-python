from datetime import time

from .database import SqlAlchemyDatbase
from .entities import AddressEntity, RestaurantEntity
from .restaurant_repository import RestaurantRepository

db = SqlAlchemyDatbase("sqlite://", False)
db.create_database()
repo = RestaurantRepository(db.managed_session)


def test_restaurant_repository_crud():

    def action(session):
        repo = RestaurantRepository.create_with_session(session)
        addr = AddressEntity()
        addr.city = "Salzburg"
        addr.country = "AT"
        addr.street = "Hauptstraße 1"
        addr.zip = 5020

        res = RestaurantEntity()
        res.name = "Test-Restaurant"
        res.open_from = time(10, 0, 0)
        res.open_until = time(22, 0, 0)
        res.open_days = "MONDAY;TUESDAY"
        res.address = addr
        saved = repo.save(res)
        repo.sync()

        all_restaurants = repo.get_all_restaurants()
        assert len(all_restaurants) == 1

        find_restaurant = repo.get_restaurant_by_id(saved.id)
        assert find_restaurant.name == res.name

        # update the name of the restaurant
        find_restaurant.name += " updated"
        repo.save(find_restaurant)

        updated_restaurant = repo.get_restaurant_by_id(find_restaurant.id)
        assert "Test-Restaurant updated" == updated_restaurant.name

        # updat the address
        updated_restaurant.address.street += " updated"
        repo.save(updated_restaurant)

        updated_address = repo.get_restaurant_by_id(updated_restaurant.id)
        assert "Hauptstraße 1 updated" == updated_address.address.street

        # lookup the address
        repo.sync()  # want to "read" within the transaction
        addr_lookup = repo.find_address(addr)
        assert addr_lookup is not None
        assert addr.street == addr_lookup.street
        assert addr.city == addr_lookup.city
        assert addr.zip == addr_lookup.zip
        assert addr.country == addr_lookup.country

    repo.unit_of_work(action)
