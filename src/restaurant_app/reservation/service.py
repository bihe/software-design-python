from ..restaurant.service import RestaurantService
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

        # 1) is the reservation date/time possible with the desired restaurant
        if not self._restaurant_svc.is_restaurant_open(
            request.restaurant_id, request.reservation_date, request.time_from, request.time_until
        ):
            raise ReservationError("could not place reservation for given date/time; restaurant not open")

        # 2) are tables available with the given capacity

        # 3) is there one table available for reservation (not an overlapping reservation)

        pass
