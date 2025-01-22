from sqlalchemy import String, Date, Time, Integer
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base(mapped_column_default_doc={
    'nullable': False
})

class BookingModel(Base):
    __tablename__ = "bookings"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user: Mapped[str] = mapped_column(String)   
    room: Mapped[str] = mapped_column(String)
    date: Mapped[Date] = mapped_column(Date)
    start_time: Mapped[Time] = mapped_column(Time)
    end_time: Mapped[Time] = mapped_column(Time) 