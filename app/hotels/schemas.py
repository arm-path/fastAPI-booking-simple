from dataclasses import dataclass
from typing import Optional, List

from fastapi import Form, UploadFile
from pydantic import BaseModel

from app.images.schemas import ImageSchema
from app.rooms.schemas import RoomListSchema


class BaseHotelSchema(BaseModel):
    id: int
    title: str
    location: str
    image: Optional[ImageSchema] = None


class ListHotelSchema(BaseHotelSchema):
    pass


class DetailHotelSchema(BaseHotelSchema):
    rooms: Optional[List[RoomListSchema]] = None


@dataclass
class HotelSchemaForm:
    title: str = Form(min_length=3, max_length=255)
    location: str = Form(max_length=255)
    image: UploadFile = None
    rooms_quantity: int = Form(default=1)


@dataclass
class UpdateSchemaForm(HotelSchemaForm):
    clean_image: bool = Form(default=False)
