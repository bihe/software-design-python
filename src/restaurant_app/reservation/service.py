import threading
from typing import List

from ..restaurant.models import TableModel
from ..restaurant.service import RestaurantService
from ..shared.random import random_with_N_digits
from ..store.entities import ReservationEntity, TableEntity
from ..store.reservation_repo import ReservationRepository
from ..store.table_repository import TableRepository
from .models import ReservationModel, ReservationRequestModel
from .service_model_mapper import mapEntityToModel


class ReservationError(Exception):
    """An error during a Reservation"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


# we need to ensure that we do not have race-conditions during reservation-process
mutex = threading.Lock()


class ReservationService:
    def __init__(
        self,
        restaurant_svc: RestaurantService,
        reservation_repo: ReservationRepository,
        table_repo: TableRepository,
    ):
        self._restaurant_svc = restaurant_svc
        self._reservation_repo = reservation_repo
        self._table_repo = table_repo

    def __str__(self) -> str:
        return "ReservationService"

    def get_reservation_for_restaurant(self, restaurant_id: int) -> List[ReservationModel]:
        """
        Return all available reservations for the given restaurant

        Returns: List of ReservationModels
        """
        reservations = self._reservation_repo.get_reservation_for_restaurant(restaurant_id)
        if reservations is None or len(reservations) == 0:
            return []

        reservation_model: List[ReservationModel] = []
        for res in reservations:
            reservation_model.append(mapEntityToModel(res))
        return reservation_model

    def reserve(self, request: ReservationRequestModel) -> ReservationModel:
        """Provide a request for a reservation date/time/number-of-people/name.
        The logic needs to find if a table is available for the given date/time-frame
        """
        reservation: ReservationModel = None

        # a parallel reservation process should not interfere
        with mutex:

            # the main task is to find a slot for the requested date/time with the given capacity
            # we will check if the restaurant is open and if there are tables available wilth the given capacity.
            # for each table which has the capacity, we determine if the table has a reservation slot available.
            # we do this by checking if the desired from-until time is not reserved, is available.

            # 1) is the reservation date/time possible with the desired restaurant
            if not self._restaurant_svc.is_restaurant_open(
                request.restaurant_id, request.reservation_date, request.time_from, request.time_until
            ):
                raise ReservationError("could not place reservation for given date/time; restaurant not open")

            # 2) are tables available with the given capacity
            avail_tables = self._table_repo.get_tables_with_capacity(request.num_people, request.restaurant_id)
            if avail_tables is None or len(avail_tables) == 0:
                raise ReservationError("could not place reservation, no tables for the given capactiy are available")

            table_to_reserve: TableEntity = None

            # 3) is there one table available for reservation (not an overlapping reservation)
            # iterate over the given tables and find out if the given slot, defined by data/time is available
            for table in avail_tables:
                # get the reservations for the given table and date
                reservations = self._reservation_repo.get_table_reservations_for_date(
                    request.reservation_date, table.id
                )
                if len(reservations) == 0:
                    # there are no reservations for the given table -> use the table for reservations
                    table_to_reserve = table
                    break

                # process the saved reservations to find a possible slot

                # +-----------+
                # |   18:00   |
                # |<---------------------------------------+-------+------------->
                # |   19:00   |                            |       |
                # |<-------------+-------+--+---+----------|-------|------------->
                # |   20:00   |  |       |  |   |          |       |
                # |<-------------|-------|--+---+--+---+---+-------+--+-------+-->
                # |   21:00   |  |       |         |   |              |       |
                # |<-------------+-------+---------+---+--------------|-------|-->
                # |   22:00   |                                       |       |
                # |<--------------------------------------------------+-------+-->
                # |   23:00   |
                # +-----------+

                for reservation in reservations:
                    # 1) check if there is a reservation for the exact from-until
                    # above: if the request is from 20:00 to 22:00
                    #           or from 20:00 to 21:00 (within from-until)
                    #           or from 21:00 to 22:00 (within from-until)
                    if request.time_from >= reservation.time_from and request.time_until <= reservation.time_until:
                        # set any found table to None, because we need to process all reservations
                        table_to_reserve = None
                        break

                    # 2) check if we have an overlap
                    # either the until_date is within an existing reservation
                    # above: if the request is from 19:00 to 21:00
                    #           and overlaps with 20:00-22:00
                    if (
                        request.time_from <= reservation.time_from
                        and request.time_until > reservation.time_from
                        and request.time_until < reservation.time_until
                    ):
                        table_to_reserve = None
                        break

                    # or the from_date is within one
                    # above: if the request is from 21:00 to 23:00
                    #           and overlaps with 20:00-22:00
                    if (
                        request.time_from >= reservation.time_from
                        and request.time_from < reservation.time_until
                        and request.time_until > reservation.time_until
                    ):
                        table_to_reserve = None
                        break

                    # if we came this far - we got us a table
                    # but it might be, that the table is set to None for the next loop iteration
                    # we need to finish the iteration, because we only look at one reseration after the other
                    # so if we have found a slot in the first iteration, it can be invalidated by the next iteration.
                    table_to_reserve = table

                # exit the outer loop of tables if we have found a table
                if table_to_reserve is not None:
                    break

            if table_to_reserve is None:
                raise ReservationError("could not place reservation, no tables available for the given date/time")

            # a table is available, store the reservation
            def work_in_transaction(session) -> List[ReservationModel]:
                reservation_repo = self._reservation_repo.new_session(session)

                reservation_number = ""
                while True:
                    reservation_number = str(random_with_N_digits(7))
                    if not reservation_repo.is_reservation_number_in_use(reservation_number):
                        break

                reservation = ReservationEntity(
                    reservation_date=request.reservation_date,
                    time_from=request.time_from,
                    time_until=request.time_until,
                    people=request.num_people,
                    reservation_name=request.name,
                    reservation_number=reservation_number,
                )
                reservation.tables.append(table_to_reserve)
                saved = reservation_repo.save(reservation)
                return [
                    ReservationModel(
                        id=saved.id,
                        number=saved.reservation_number,
                        name=saved.reservation_name,
                        num_people=saved.people,
                        time_from=saved.time_from,
                        time_until=saved.time_until,
                        reservation_date=saved.reservation_date,
                        reserved_table=TableModel(
                            id=saved.tables[0].id, number=saved.tables[0].table_number, places=saved.tables[0].seats
                        ),
                    )
                ]

            result = self._reservation_repo.unit_of_work(work_in_transaction)
            reservation = result[0]
        return reservation
