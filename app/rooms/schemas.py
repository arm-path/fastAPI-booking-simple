from dataclasses import dataclass
from typing import Optional

from fastapi import Form, UploadFile
from pydantic import BaseModel

from app.images.schemas import ImageSchema


class BaseRoomSchema(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    price: int
    quantity: int
    image: Optional[ImageSchema] = None


class RoomListSchema(BaseRoomSchema):
    pass


class RoomDetailSchema(BaseRoomSchema):
    hotel_id: int


@dataclass
class BaseRoomForm:
    title: str = Form(min_length=3, max_length=255)
    description: str = Form(default=None)
    price: int = Form(ge=0, default=0)
    quantity: int = Form(default=1)
    image: UploadFile = None


@dataclass
class CreateRoomSchemaForm(BaseRoomForm):
    hotel_id: int = Form()


@dataclass
class UpdateRoomSchemaForm(BaseRoomForm):
    clean_image: bool = Form(default=False)
