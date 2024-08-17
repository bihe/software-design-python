from dataclasses import dataclass

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


@dataclass
class RestaurantModel(Base):
    __tablename__ = "RESTAURANT"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column("name", String(255))
