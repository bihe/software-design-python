from abc import ABC, abstractmethod
from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session


class BaseRepository(ABC):

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]], session: Session = None):
        """
        provide a factory to create sessions or pass in an existing session
        """
        self._session_factory = session_factory
        self._session = session

    def get_session(self) -> Session:
        # if we have an existing session return it
        # otherwise use the factory to create one
        if self._session is not None:
            return self._session
        return self._session_factory()

    def unit_of_work(self, action: Callable[[Session], None]):
        with self._session_factory() as session:
            with session.begin():
                action(session)

    def sync(self):
        self._session.flush()

    @classmethod
    @abstractmethod
    def create_with_session(cls):
        pass
