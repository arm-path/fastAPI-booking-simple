from datetime import date

from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import aliased

from app.bookings.models import Bookings
from app.database import session
from app.rooms.models import Rooms
from app.services.database import DatabaseService


class BookingService(DatabaseService):
    model = Bookings

    @classmethod
    async def check_available_rooms(cls, room_id: int, date_from: date, date_to: date):
        """
            -- ДАТА ЗАЕЗДА 2023-06-10
            -- ДАТА ВЫЕЗДА 2023-06-18

            WITH booking as (SELECT * FROM bookings
            WHERE room_id = 1 AND (
                (date_from > '2023-06-10' AND date_from < '2023-06-18') OR
                (date_from < '2023-06-10' AND date_to < '2023-06-18')
            ))

            SELECT rooms.title, (rooms.quantity - COUNT(rooms.id)) as remainder, rooms.price 
            FROM rooms 
            LEFT JOIN booking ON booking.room_id = rooms.id
            WHERE rooms.id = 1
            GROUP BY rooms.id, rooms.title, rooms.price
        """
        async with session() as conn:
            occupied_rooms = (select(Bookings)
                              .where(and_(room_id == room_id,
                                          or_(and_(Bookings.date_from >= date_from, Bookings.date_from <= date_to),
                                              and_(Bookings.date_from <= date_from, Bookings.date_to > date_from))))
                              .cte('occupied_rooms'))
            r = aliased(Rooms)
            available_rooms = (
                select(r.id, r.title, (r.quantity - func.count(occupied_rooms.c.id)).label('remainder'), r.price)
                    .select_from(r)
                    .outerjoin(occupied_rooms, r.id == occupied_rooms.c.room_id)
                    .where(r.id == room_id)
                    .group_by(r.id, r.title, r.price)
            )
            available_rooms = await conn.execute(available_rooms)
            return available_rooms.mappings().one_or_none()
