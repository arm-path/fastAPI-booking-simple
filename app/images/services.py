from sqlalchemy import insert

from app.database import session
from app.images.models import Images
from app.services.database import DatabaseService
from app.services.image import ImageBaseService


class ImageService(DatabaseService):
    model = Images

    @classmethod
    async def create_image_and_miniature(cls, image_model, image):
        image_info = ImageBaseService.get_image_info(image_model.__tablename__, image)
        ImageBaseService.save_image(image_info['image_url'], image)
        ImageBaseService.miniature_image(image_info, image, 200)
        async with session() as conn:
            stmt = (insert(cls.model)
                    .values(title=image_info['image_name'], upload_to=image_info['image_url'])
                    .returning(cls.model.id))
            image_id = await conn.execute(stmt)
            await conn.commit()
            return image_id.mappings().one_or_none()['id']
