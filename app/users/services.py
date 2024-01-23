from sqlalchemy import select

from app.database import session
from app.services.database import DatabaseService
from app.users.models import Users


class UserService(DatabaseService):
    model = Users

    @classmethod
    async def get_user(cls, id):
        async with session() as conn:
            query = select(cls.model.id, cls.model.email, cls.model.installer).select_from(cls.model).filter_by(id=id)
            user = await conn.execute(query)
            user = user.mappings().one_or_none()
            return user
