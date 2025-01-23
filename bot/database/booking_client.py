from database import get_db
from schemas import BookingSchema
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
import datetime
from typing import List, Optional, Tuple

class BookingClient:
    def __init__(self):
        pass

    async def create_booking(self, booking: BookingSchema) -> Tuple[Optional[BookingSchema], Optional[str]]:
        """Create a new booking in the database.

        Args:
            booking: The booking to create

        Returns:
            Tuple containing:
            - BookingSchema if successful, None if failed
            - Error message if failed, None if successful
        """
        async for session in get_db():
            try:
                session.add(booking)
                await session.commit()
                await session.refresh(booking)
                return booking, None
            except Exception as e:
                await session.rollback()
                return None, str(e)

    async def get_bookings_by_date(self, date: datetime.date) -> Tuple[Optional[List[BookingSchema]], Optional[str]]:
        """Get all bookings for a specific date.

        Args:
            date: The date to query bookings for

        Returns:
            Tuple containing:
            - List of bookings if successful, None if failed
            - Error message if failed, None if successful
        """
        async for session in get_db():
            try:
                result = await session.execute(
                    select(BookingSchema).where(BookingSchema.date == date)
                )
                return result.scalars().all(), None
            except Exception as e:
                return None, str(e)
    
    async def update_booking(self, booking: BookingSchema) -> Tuple[Optional[BookingSchema], Optional[str]]:
        """Update an existing booking.

        Args:
            booking: The booking with updated information

        Returns:
            Tuple containing:
            - Updated booking if successful, None if failed
            - Error message if failed, None if successful
        """
        async for session in get_db():
            try:
                updated_booking = await session.merge(booking)
                await session.commit()
                return updated_booking, None
            except Exception as e:
                await session.rollback()
                return None, str(e)

    async def delete_booking(self, booking_id: int) -> Tuple[bool, Optional[str]]:
        """Delete a booking by its ID.

        Args:
            booking_id: The ID of the booking to delete

        Returns:
            Tuple containing:
            - Boolean indicating if deletion was successful
            - Error message if failed, None if successful
        """
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
                return False, str(e)

booking_client = BookingClient()
