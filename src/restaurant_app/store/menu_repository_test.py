from typing import Any, List

from .entities import MenuEntity
from .menu_repository import MenuRepository
from .repository_test_helpers import create_restaurant_data, get_database
from .restaurant_repository import RestaurantRepository


def test_menu_repository_crud():

    def action(session) -> List[Any]:
        res_repo = RestaurantRepository.create_with_session(session)
        menu_repo = MenuRepository.create_with_session(session)

        res = create_restaurant_data()
        res = res_repo.save(res)
        res_repo.sync()

        menu = MenuEntity(name="MenuEntry1", category="Category1", price=14.50, restaurant=res)
        menu = menu_repo.save(menu)

        menu_lookup = menu_repo.get_menu_by_name("MenuEntry1", res.id)
        assert menu_lookup is not None
        assert menu_lookup.category == menu.category
        assert menu_lookup.price == menu.price

        menus = menu_repo.get_menu_list(res.id)
        assert len(menus) == 1
        result = []
        result.append(res.id)
        return result

    repo = MenuRepository(get_database().managed_session)
    _ = repo.unit_of_work(action)

    # menus = repo.get_menu_list(result[0])
    # assert len(menus) == 1
