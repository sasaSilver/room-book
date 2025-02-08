from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from functools import wraps
from typing import List
from bot.database.core import async_session
from bot.database.schemas import BookingSchema, AdminSchema
import datetime

def inject_session(func):
    """
    Injects session object to the decorated db method.
    You do not need to pass it manually.
    """
    @wraps(func)
    async def wrapper(*args):
        async with async_session() as session:
            try:
                session.begin()
                return await func(session, *args)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.commit()
                await session.close()
                
    return wrapper

@inject_session
async def create_booking(session: AsyncSession, booking: BookingSchema) -> BookingSchema:
    session.add(booking)
    return booking
    
@inject_session
async def get_bookings_by_date_room(session: AsyncSession, date: datetime.date, room: str) -> List[BookingSchema]:
    result = await session.execute(
        select(BookingSchema).where(BookingSchema.date == date, BookingSchema.room == room)
    )
    return result.scalars().all()

@inject_session
async def get_booking_by_id(session: AsyncSession, booking_id: int) -> BookingSchema:
    result = await session.execute(
        select(BookingSchema).where(BookingSchema.id == booking_id)
    )
    return result.scalar()

@inject_session
async def get_bookings_by_username(session: AsyncSession, username: str) -> List[BookingSchema]:
    result = await session.execute(
        select(BookingSchema).
        where(BookingSchema.username == username).
        order_by(BookingSchema.date).
        order_by(BookingSchema.start_time)
    )
    return result.scalars().all()

@inject_session
async def get_bookings_by_room(session: AsyncSession, room: str) -> List[BookingSchema]:
    result = await session.execute(
        select(BookingSchema).
        where(BookingSchema.room == room).
        order_by(BookingSchema.date).
        order_by(BookingSchema.start_time)
    )
    return result.scalars().all()

@inject_session
async def delete_booking_by_id(session: AsyncSession, booking_id: int) -> None:
    await session.execute(
        delete(BookingSchema).where(BookingSchema.id == booking_id)
    )

@inject_session
async def delete_all_bookings_by_username(session: AsyncSession, username: str) -> None:
    await session.execute(
        delete(BookingSchema).where(BookingSchema.username == username)
    )

@inject_session
async def get_all_bookings(session: AsyncSession) -> List[BookingSchema]:
    result = await session.execute(select(BookingSchema))
    return result.scalars().all()

@inject_session
async def add_admin(session: AsyncSession, id: int, username: str) -> AdminSchema:
    admin = AdminSchema(
        username=username,
        id=id
    )
    session.add(admin)
    return admin
    
@inject_session
async def get_admins(session: AsyncSession) -> List[AdminSchema]:
    result = await session.execute(select(AdminSchema))
    return result.scalars().all()

@inject_session
async def is_admin(session: AsyncSession, username: str, id: int) -> bool:
    result = None
    if username:
        result = await session.execute(select(AdminSchema).where(AdminSchema.username == username))
    elif id:
        result = await session.execute(select(AdminSchema).where(AdminSchema.id == id))
    
    return result.scalar() is not None
    
if __name__ == "__main__":
    import asyncio
    print(asyncio.run(get_admins()))
