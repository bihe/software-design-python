from .repository_test_helpers import create_restaurant_data, get_database
from .restaurant_repository import RestaurantRepository


def test_restaurant_repository_crud():

    def action(session):
        res = create_restaurant_data()
        addr = res.address
        repo = RestaurantRepository.create_with_session(session)
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

    db = get_database()
    repo = RestaurantRepository(db.managed_session)
    repo.unit_of_work(action)

    all_restaurants = repo.get_all_restaurants()
    assert len(all_restaurants) == 1
