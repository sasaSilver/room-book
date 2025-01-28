from sqlalchemy import String, Date, Time, Integer, Index, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

class Base(DeclarativeBase):
    ...

class BookingSchema(Base):
    __tablename__ = "bookings"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    user_full_name: Mapped[str] = mapped_column(String, nullable=False)
    room: Mapped[str] = mapped_column(String, nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    start_time: Mapped[Time] = mapped_column(Time, nullable=False)
    end_time: Mapped[Time] = mapped_column(Time, nullable=False)
    
    __table_args__ = (
        Index('idx_username', 'username'),
        Index('idx_room_date', 'room', 'date'),
        CheckConstraint('end_time > start_time', name='check_time_order'),
        CheckConstraint(date >= func.current_date(), name='check_future_date'),
    )