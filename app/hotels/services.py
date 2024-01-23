from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import session
from app.hotels.models import Hotels
from app.rooms.models import Rooms
from app.services.database import DatabaseService


class HotelsService(DatabaseService):
    model = Hotels

    @classmethod
    async def get_hotel_with_rooms_by_id(cls, id: int):
        async with session() as conn:
            query = (select(cls.model)
                     .where(cls.model.id == id)
                     .options(selectinload(cls.model.image),
                              selectinload(cls.model.rooms).options(selectinload(Rooms.image))))
            obj = await conn.execute(query)
            return obj.scalar_one_or_none()
