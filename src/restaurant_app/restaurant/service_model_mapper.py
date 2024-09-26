from datetime import time
from typing import List

from ..store.entities import RestaurantEntity
from .models import AddressModel, MenuModel, RestaurantModel, TableModel, WeekDay

_LIST_DELIMINATOR = ";"


def mapDayFromEnum(days: List[WeekDay]) -> str:
    db_days: List[str] = []
    for day in days:
        db_days.append(str(day))
    return _LIST_DELIMINATOR.join(db_days)


def mapDayToEnum(openDays: str) -> List[WeekDay]:
    days: List[WeekDay] = []
    for day in openDays.split(_LIST_DELIMINATOR):
        match day:
            case "MONDAY":
                days.append(WeekDay.MONDAY)
            case "TUESDAY":
                days.append(WeekDay.TUESDAY)
            case "WEDNESDAY":
                days.append(WeekDay.WEDNESDAY)
            case "THURSDAY":
                days.append(WeekDay.THURSDAY)
            case "FRIDAY":
                days.append(WeekDay.FRIDAY)
            case "SATURDAY":
                days.append(WeekDay.SATURDAY)
            case "SUNDAY":
                days.append(WeekDay.SUNDAY)
    return days


def mapEntityToModel(res: RestaurantEntity) -> RestaurantModel:
    open_days = mapDayToEnum(res.open_days)

    def _mapTimeToHours(t: time) -> List[int]:
        times: List[int] = []
        times.append(t.hour)
        times.append(t.minute)
        return times

    restaurant_model = RestaurantModel(
        id=res.id,
        id_hash="",
        address=AddressModel(
            street=res.address.street,
            zip=res.address.zip,
            city=res.address.city,
            country_code=res.address.country,
        ),
        menus=None,
        tables=None,
        name=res.name,
        open_from=_mapTimeToHours(res.open_from),
        open_until=_mapTimeToHours(res.open_until),
        open_days=open_days,
    )

    # map to MenuModel
    if res.menus is not None:
        menus: List[MenuModel] = []
        for menu in res.menus:
            menu_model = MenuModel(id=menu.id, name=menu.name, price=menu.price, category=menu.category)
            menus.append(menu_model)
        restaurant_model.menus = menus

    # map to TableModel
    if res.tables is not None:
        tables: List[TableModel] = []
        for table in res.tables:
            table_model = TableModel(id=table.id, number=table.table_number, places=table.seats)
            tables.append(table_model)
        restaurant_model.tables = tables

    return restaurant_model
