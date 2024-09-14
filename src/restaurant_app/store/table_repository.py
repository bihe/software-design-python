import datetime
from contextlib import AbstractContextManager
from typing import Callable, List, Self

from sqlalchemy.orm import Session

from .base_repository import BaseRepository
from .entities import TableEntity


class TableRepository(BaseRepository):

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]], session: Session = None):
        super().__init__(session_factory=session_factory, session=session)

    @classmethod
    def create_with_session(cls, session: Session) -> Self:
        return TableRepository(session_factory=None, session=session)

    def get_table_by_id(self, id: int) -> TableEntity:
        with self.get_session() as session:
            return session.get(TableEntity, id)

    def get_tables_for_restaurant(self, restaurant_id: int) -> List[TableEntity]:
        with self.get_session() as session:
            return session.query(TableEntity).filter(TableEntity.retaurant_id == restaurant_id).all()

    def save(self, table: TableEntity) -> TableEntity:
        with self.get_session() as session:
            table_id = table.id or 0
            if table_id > 0:
                existing = session.get(TableEntity, table_id)
                if existing is not None:
                    existing.table_number = table.table_number
                    existing.modified = datetime.datetime.now(datetime.UTC)
                    existing.retaurant = table.restaurant
                    session.add(existing)
                    return existing
            else:
                # lookup the table by its number
                existing = (
                    session.query(TableEntity)
                    .filter(TableEntity.table_number == table.table_number)
                    .filter(TableEntity.retaurant_id == table.restaurant.id)
                    .first()
                )
                if existing is not None:
                    existing.table_number = table.table_number
                    existing.modified = datetime.datetime.now(datetime.UTC)
                    session.add(existing)
                    return existing

            # new or not found
            session.add(table)
            session.flush()
        return table
