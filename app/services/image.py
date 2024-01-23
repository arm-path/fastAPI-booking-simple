import shutil
from datetime import datetime
from typing import Optional

from PIL import Image, UnidentifiedImageError
from fastapi import UploadFile

from app.exceptions import InvalidImageFileException
from app.logging import logger


class ImageBaseService:
    @classmethod
    def get_image_info(cls, dir_name: str, image: Optional[UploadFile]):
        if not image.headers['content-type'] in ['image/png', 'image/jpeg', 'image/webp']:
            logger.error('Attempt load invalid image.')
            raise InvalidImageFileException
        try:
            Image.open(image.file)
        except UnidentifiedImageError:
            logger.error('Attempt load invalid image.')
            raise InvalidImageFileException
        image_extension = image.filename.split('.')[-1]
        image_name = dir_name + '_' + str(int(datetime.utcnow().timestamp()))
        image_url = f'images/{dir_name}/{image_name}.{image_extension}'
        return {'image_name': image_name, 'image_url': image_url}

    @classmethod
    def save_image(cls, image_url, image: Optional[UploadFile]):
        with open(f'app/static/{image_url}', 'wb+') as file:
            shutil.copyfileobj(image.file, file)

    @classmethod
    def miniature_image(cls, image_info: dict, image: UploadFile, width: int):
        image_name = f'min_{image_info["image_name"]}.{image.filename.split(".")[-1]}'
        image_url = image_info['image_url'].replace(image_info['image_url'].split("/")[-1], image_name)
        try:
            img = Image.open(image.file)
            fixed_width = 200
            width_percent = (fixed_width / float(img.size[0]))
            height_size = int((float(img.size[0]) * float(width_percent)))
            miniature = img.resize((fixed_width, height_size))
            miniature.save(f'app/static/{image_url}')
        except UnidentifiedImageError:
            logger.error('Attempt load invalid image.')
            raise InvalidImageFileException
        except Exception as err:
            logger.error('Failed to save image', extra={'error': err})
            raise InvalidImageFileException
