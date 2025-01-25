from bot.database import get_db
from bot.database.schemas import BookingSchema
from sqlalchemy import select, delete
import datetime, asyncio
from typing import List, Optional, Tuple

class BookingClient:
    def __init__(self):
        pass

    async def create_booking(self, booking: BookingSchema) -> Tuple[bool, Optional[Exception]]:
        async for session in get_db():
            try:
                session.add(booking)
                await session.commit()
                return True, None
            except Exception as e:
                await session.rollback()
                return False, e
    
    async def get_bookings_by_date(self, date: datetime.date, room: str) -> Tuple[bool, Optional[List[BookingSchema]], Optional[Exception]]:
        async for session in get_db():
            try:
                result = await session.execute(
                    select(BookingSchema).where(BookingSchema.date == date, BookingSchema.room == room)
                )
                return True, result.scalars().all(), None
            except Exception as e:
                return False, None, e
            
    async def get_bookings_by_username(self, username: str) -> Tuple[bool, Optional[List[BookingSchema]], Optional[Exception]]:
        async for session in get_db():
            try:
                result = await session.execute(
                    select(BookingSchema).where(BookingSchema.username == username)
                )
                return True, result.scalars().all(), None
            except Exception as e:
                return False, None, e
    
    async def delete_booking(self, booking_id: int) -> Tuple[bool, Optional[Exception]]:
        async for session in get_db():
            try:
                result = await session.execute(
                    delete(BookingSchema).where(BookingSchema.id == booking_id)
                )
                await session.commit()
                if result.rowcount > 0:
                    return True, None
                else:
                    return False, None
            except Exception as e:
                await session.rollback()
                return False, e

booking_client = BookingClient()

if __name__ == "__main__":
    asyncio.run(booking_client.get_bookings_by_date(datetime.date.today()))
