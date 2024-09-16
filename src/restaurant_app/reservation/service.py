from ..restaurant.service import RestaurantService
from ..store.entities import TableEntity
from ..store.reservation_repo import ReservationRepository
from ..store.table_repository import TableRepository
from .models import ReservationModel, ReservationRequestModel


class ReservationError(Exception):
    """An error during a Reservation"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


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

    def reserve(self, request: ReservationRequestModel) -> ReservationModel:
        """Provide a request for a reservation date/time/number-of-people/name.
        The logic needes to find if a table is available for the given date/time-frame
        """

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
            reservations = self._reservation_repo.get_table_reservations_for_date(request.reservation_date, table.id)
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
                    continue

                # 2) check if we have an overlap
                # either the until_date is within an existing reservation
                # above: if the request is from 19:00 to 21:00
                #           and overlaps with 20:00-22:00
                if (
                    request.time_from < reservation.time_from
                    and request.time_until > reservation.time_from
                    and request.time_until < reservation.time_until
                ):
                    table_to_reserve = None
                    continue

                # or the from_date is within one
                # above: if the request is from 21:00 to 23:00
                #           and overlaps with 20:00-22:00
                if (
                    request.time_from > reservation.time_from
                    and request.time_from < reservation.time_until
                    and request.time_until > reservation.time_until
                ):
                    table_to_reserve = None
                    continue

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

        return None
