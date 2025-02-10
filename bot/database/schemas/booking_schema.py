import datetime

from sqlalchemy import String, Date, Time, Integer, func
from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from bot.database.schemas.base import Base


class BookingSchema(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False, index=True)
    user_full_name: Mapped[str] = mapped_column(String, nullable=False)
    room: Mapped[str] = mapped_column(String, nullable=False, index=True)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False, index=True)
    start_time: Mapped[datetime.time] = mapped_column(Time, nullable=False)
    end_time: Mapped[datetime.time] = mapped_column(Time, nullable=False)

    __table_args__ = (
        CheckConstraint("end_time > start_time", name="check_time_order"),

        # костыль, хз как проверить, чтобы таймслоты не пересекались
        # TODO: добавить проверку на пересечение таймслотов
        UniqueConstraint(
            "room", "date", "start_time", name="unique_room_date_start_time"
        ),
        UniqueConstraint(
            "room", "date", "end_time", name="unique_room_date_end_time"
        ),
    )
