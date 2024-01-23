from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import selectinload

from app.database import session
from app.images.models import Images
from app.services.image import ImageBaseService


class DatabaseService:
    model = None
    model_image = Images

    @classmethod
    async def get_list(cls, **filter):
        async with session() as conn:
            query = select(cls.model).filter_by(**filter)
            objects = await conn.execute(query)
            return objects.scalars().all()

    @classmethod
    async def get_object(cls, **filter):
        async with session() as conn:
            query = select(cls.model).filter_by(**filter)
            obj = await conn.execute(query)
            return obj.scalar_one_or_none()

    @classmethod
    async def get_object_by_id(cls, id: int):
        async with session() as conn:
            query = select(cls.model).filter_by(id=id)
            obj = await conn.execute(query)
            return obj.scalar_one_or_none()

    @classmethod
    async def create_object(cls, **data):
        async with session() as conn:
            stmt = insert(cls.model).values(**data).returning(cls.model.id)
            obj = await conn.execute(stmt)
            await conn.commit()
            return obj.mappings().one_or_none()

    @classmethod
    async def update_object(cls, id: int, **data):
        async with session() as conn:
            stmt = update(cls.model).where(cls.model.id == id).values(**data)
            await conn.execute(stmt)
            await conn.commit()

    @classmethod
    async def delete_object_by_id(cls, id: int):
        async with session() as conn:
            stmt = delete(cls.model).where(cls.model.id == id)
            await conn.execute(stmt)
            await conn.commit()

    @classmethod
    async def get_image_info(cls, tablename, image):
        image_info = ImageBaseService.get_image_info(tablename, image)
        image_info['stmt'] = (insert(Images)
                              .values(title=image_info['image_name'], upload_to=image_info['image_url'])
                              .returning(Images.id))
        return image_info

    @classmethod
    async def get_list_with_image_field(cls, **filter):
        async with session() as conn:
            query = select(cls.model).filter_by(**filter).options(selectinload(cls.model.image))
            objects = await conn.execute(query)
            return objects.scalars().all()

    @classmethod
    async def get_object_with_image_field(cls, id):
        async with session() as conn:
            query = select(cls.model).where(cls.model.id == id).options(selectinload(cls.model.image))
            obj = await conn.execute(query)
            return obj.scalar_one_or_none()

    @classmethod
    async def create_object_with_image_field(cls, **values):
        image = values.pop('image')
        async with session() as conn:
            if image:
                image_info = await cls.get_image_info(cls.model.__tablename__, image)
                image_stmt_result = await conn.execute(image_info['stmt'])
                values['image_id'] = image_stmt_result.mappings().one_or_none()['id']
            stmt = (insert(cls.model)
                    .values(**values)
                    .returning(cls.model)
                    .options(selectinload(cls.model.image)))
            result_obj = await conn.execute(stmt)
            if image:
                ImageBaseService.save_image(image_info['image_url'], image)
            await conn.commit()
            return result_obj.mappings().one_or_none()

    @classmethod
    async def update_object_with_image_field(cls, obj, **values):
        image = values.pop('image')
        clean_image = values.pop('clean_image')
        async with session() as conn:
            if image:
                image_info = await cls.get_image_info(cls.model.__tablename__, image)
                image_stmt_result = await conn.execute(image_info['stmt'])
                values['image_id'] = image_stmt_result.mappings().one_or_none()['id']
            else:
                values['image_id'] = None if clean_image else obj.image_id
            stmt = (update(cls.model)
                    .where(cls.model.id == obj.id)
                    .values(**values).returning(cls.model)
                    .options(selectinload(cls.model.image)))
            result_obj = await conn.execute(stmt)
            if image:
                ImageBaseService.save_image(image_info['image_url'], image)
            await conn.commit()
            return result_obj.mappings().one_or_none()
