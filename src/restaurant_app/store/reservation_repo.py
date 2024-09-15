import datetime
from contextlib import AbstractContextManager
from typing import Callable, Self

from sqlalchemy.orm import Session

from .base_repository import BaseRepository
from .entities import ReservationEntity


class ReservationRepository(BaseRepository):

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]], session: Session = None):
        super().__init__(session_factory=session_factory, session=session)

    @classmethod
    def create_with_session(cls, session: Session) -> Self:
        return ReservationRepository(session_factory=None, session=session)

    def save(self, reservation: ReservationEntity) -> ReservationEntity:
        with self.get_session() as session:
            reservation_id = reservation.id or 0
            if reservation_id > 0:
                existing = session.get(ReservationEntity, reservation_id)
                if existing is not None:
                    existing.reservation_name = reservation.reservation_name
                    existing.reservation_number = reservation.reservation_number
                    existing.reservation_date = reservation.reservation_date
                    existing.people = reservation.people
                    existing.time_from = reservation.time_from
                    existing.time_until = reservation.time_until
                    existing.modified = datetime.datetime.now(datetime.UTC)
                    session.add(existing)
                    return existing
            else:
                # lookup the reservation by its number
                existing = (
                    session.query(ReservationEntity)
                    .filter(ReservationEntity.reservation_number == reservation.reservation_number)
                    .first()
                )
                if existing is not None:
                    existing.reservation_name = reservation.reservation_name
                    existing.reservation_date = reservation.reservation_date
                    existing.people = reservation.people
                    existing.time_from = reservation.time_from
                    existing.time_until = reservation.time_until
                    existing.modified = datetime.datetime.now(datetime.UTC)
                    session.add(existing)
                    return existing

            # new or not found
            session.add(reservation)
            session.flush()
        return reservation

    def get_reservation_by_id(self, id: int) -> ReservationEntity:
        with self.get_session() as session:
            return session.get(ReservationEntity, id)

    def get_reservation_by_number(self, number: int) -> ReservationEntity:
        with self.get_session() as session:
            return session.query(ReservationEntity).filter(ReservationEntity.reservation_number == number).first()

    def is_reservation_number_in_use(self, number: str) -> bool:
        with self.get_session() as session:
            if (
                session.query(ReservationEntity.reservation_number)
                .filter(ReservationEntity.reservation_number == number)
                .scalar()
                is None
            ):
                return False
            return True
