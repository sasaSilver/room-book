from functools import wraps
from typing import List
from bot.database.core import AsyncSessionManager
from bot.database.schemas import BookingSchema
from sqlalchemy import select, delete
import datetime
from sqlalchemy.ext.asyncio import AsyncSession

def db_operation(func):
    """
    Decorator for db operations (for cleaner code)
    """
    @wraps(func)
    async def wrapper(*args):
        async with AsyncSessionManager() as session:
            return await func(session, *args)
    return wrapper

@db_operation
async def create_booking(session: AsyncSession, booking: BookingSchema) -> None:
    session.add(booking)
    return booking
    
@db_operation
async def get_bookings_by_date_room(session: AsyncSession, date: datetime.date, room: str) -> List[BookingSchema]:
    result = await session.execute(
        select(BookingSchema).where(BookingSchema.date == date, BookingSchema.room == room)
    )
    return result.scalars().all()

@db_operation
async def get_booking_by_id(session: AsyncSession, booking_id: int) -> BookingSchema:
    result = await session.execute(
        select(BookingSchema).where(BookingSchema.id == booking_id)
    )
    return result.scalars().first()

@db_operation
async def get_bookings_by_username(session: AsyncSession, username: str) -> List[BookingSchema]:
    result = await session.execute(
        select(BookingSchema).
        where(BookingSchema.username == username).
        order_by(BookingSchema.date).
        order_by(BookingSchema.start_time)
    )
    return result.scalars().all()

@db_operation
async def delete_booking(session: AsyncSession, booking_id: int) -> None:
    await session.execute(
        delete(BookingSchema).where(BookingSchema.id == booking_id)
    )

@db_operation
async def _delete_all_bookings_by_username(session: AsyncSession, username: str) -> None:
    await session.execute(
        delete(BookingSchema).where(BookingSchema.username == username)
    )

@db_operation
async def _get_all_bookings(session: AsyncSession) -> List[BookingSchema]:
    result = await session.execute(select(BookingSchema))
    return result.scalars().all()

if __name__ == "__main__":
    import asyncio
    asyncio.run(get_bookings_by_date_room(datetime.date.today(), "1"))
