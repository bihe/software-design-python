import datetime
from dataclasses import dataclass
from typing import List

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base

relation_menu_order = Table(
    "REL_MENU_ORDER",
    Base.metadata,
    Column("menu_id", ForeignKey("MENU.id"), primary_key=True),
    Column("order_id", ForeignKey("TABLE_ORDER.id"), primary_key=True),
)

relation_table_reservation = Table(
    "REL_TABLE_RESERVATION",
    Base.metadata,
    Column("table_id", ForeignKey("GUEST_TABLE.id"), primary_key=True),
    Column("reservation_id", ForeignKey("RESERVATION.id"), primary_key=True),
)


@dataclass
class RestaurantEntity(Base):
    __tablename__ = "RESTAURANT"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column("name", String(255))
    open_from: Mapped[datetime.time] = mapped_column("open_from")
    open_until: Mapped[datetime.time] = mapped_column("open_until")
    # a deliminated list of week-days the restaurant is open
    open_days: Mapped[str] = mapped_column("open_days", String(255))

    address_id: Mapped[int] = mapped_column(ForeignKey("ADDRESS.id"))
    address: Mapped["AddressEntity"] = relationship(back_populates="restaurants")

    menus: Mapped[List["MenuEntity"]] = relationship(back_populates="restaurant")
    tables: Mapped[List["TableEntity"]] = relationship(back_populates="restaurant")


@dataclass
class AddressEntity(Base):
    __tablename__ = "ADDRESS"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    street: Mapped[str] = mapped_column("street", String(255))
    city: Mapped[str] = mapped_column("city", String(255))
    zip: Mapped[str] = mapped_column("zip", String(25))
    country: Mapped[str] = mapped_column("country", String(2))

    restaurants: Mapped[List["RestaurantEntity"]] = relationship(back_populates="address")


@dataclass
class MenuEntity(Base):
    __tablename__ = "MENU"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column("name", String(255))
    price: Mapped[float] = mapped_column("price")
    category: Mapped[str] = mapped_column("category", String(255))

    retaurant_id: Mapped[int] = mapped_column(ForeignKey("RESTAURANT.id"))
    restaurant: Mapped["RestaurantEntity"] = relationship(back_populates="menus")

    orders: Mapped[List["OrderEntity"]] = relationship(secondary=relation_menu_order, back_populates="menus")


@dataclass
class TableEntity(Base):
    __tablename__ = "GUEST_TABLE"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    table_number: Mapped[str] = mapped_column("table_number", String(255))
    seats: Mapped[int] = mapped_column("seats")

    retaurant_id: Mapped[int] = mapped_column(ForeignKey("RESTAURANT.id"))
    restaurant: Mapped[RestaurantEntity] = relationship(back_populates="tables")

    reservations: Mapped[List["ReservationEntity"]] = relationship(
        secondary=relation_table_reservation, back_populates="tables"
    )

    orders: Mapped[List["OrderEntity"]] = relationship(back_populates="table")


@dataclass
class ReservationEntity(Base):
    __tablename__ = "RESERVATION"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    reservation_date: Mapped[datetime.datetime] = mapped_column("reservation_date")
    time_from: Mapped[datetime.time] = mapped_column("time_from")
    time_until: Mapped[datetime.time] = mapped_column("time_until")
    people: Mapped[int] = mapped_column("people")
    reservation_name: Mapped[str] = mapped_column("reservation_name", String(255))
    reservation_number: Mapped[str] = mapped_column("reservation_number", String(10))

    tables: Mapped[List["TableEntity"]] = relationship(
        secondary=relation_table_reservation, back_populates="reservations"
    )


@dataclass
class OrderEntity(Base):
    __tablename__ = "TABLE_ORDER"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    total: Mapped[float] = mapped_column("total")
    waiter: Mapped[str] = mapped_column("waiter", String(255))

    table_id: Mapped[int] = mapped_column(ForeignKey("GUEST_TABLE.id"))
    table: Mapped["TableEntity"] = relationship(back_populates="orders")

    menus: Mapped[List["MenuEntity"]] = relationship(secondary=relation_menu_order, back_populates="orders")
