from fastapi import APIRouter, UploadFile, Depends

from app.exceptions import NotFoundHotelException
from app.hotels.services import HotelsService
from app.images.services import ImageService
from app.rooms.services import RoomService
from app.services.image import ImageBaseService

router = APIRouter(
    prefix='/image',
    tags=['Изображения']
)


async def base_image_create(service, obj_id, image):
    obj = await service.get_object_by_id(obj_id)
    if not obj:
        raise NotFoundHotelException
    image_id = await ImageService.create_image_and_miniature(obj, image)
    await service.update_object(id=obj_id, image_id=image_id)
    return await service.get_object_with_image_field(obj_id)


@router.post('/create-for-hotel/{hotel_id}')
async def image_create_for_hotel(hotel_id: int, image: UploadFile):
    return await base_image_create(HotelsService, hotel_id, image)


@router.post('/create-for-room/{room_id}')
async def room_create_for_room(room_id: int, image: UploadFile):
    return await base_image_create(RoomService, room_id, image)
