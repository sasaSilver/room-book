from functools import wraps
from typing import Callable, Optional, Tuple, List, TypeVar, Protocol, Awaitable, Any
from bot.database.core import AsyncSessionManager
from bot.database.schemas import BookingSchema
from sqlalchemy import select, delete
import datetime
from sqlalchemy.ext.asyncio import AsyncSession

def db_operation(func):
    """Decorator to handle database session management and error handling"""
    @wraps(func)
    async def wrapper(*args):
        async with AsyncSessionManager() as session:
            return await func(session, *args)
    
    return wrapper

@db_operation
async def create_booking(session: AsyncSession, booking: BookingSchema) -> None:
    session.add(booking)
    
@db_operation
async def get_bookings_by_date_room(session: AsyncSession, date: datetime.date, room: str) -> List[BookingSchema]:
    result = await session.execute(
        select(BookingSchema).where(BookingSchema.date == date, BookingSchema.room == room)
    )
    return result.scalars().all()

@db_operation
async def get_bookings_by_username(session: AsyncSession, username: str) -> List[BookingSchema]:
    result = await session.execute(
        select(BookingSchema).where(BookingSchema.username == username)
    )
    return result.scalars().all()

@db_operation
async def delete_booking(session: AsyncSession, booking_id: int) -> None:
    await session.execute(
        delete(BookingSchema).where(BookingSchema.id == booking_id)
    )
    await session.commit()

@db_operation
async def _delete_all_bookings_by_username(session: AsyncSession, username: str) -> None:
    await session.execute(
        delete(BookingSchema).where(BookingSchema.username == username)
    )
    await session.commit()

@db_operation
async def _get_all_bookings(session: AsyncSession) -> List[BookingSchema]:
    result = await session.execute(select(BookingSchema))
    return result.scalars().all()

if __name__ == "__main__":
    import asyncio
    asyncio.run(get_bookings_by_date_room(datetime.date.today(), "1"))
