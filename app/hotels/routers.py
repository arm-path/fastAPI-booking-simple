from typing import List

from fastapi import APIRouter, Depends

from app.authentication.services import get_user_is_installer
from app.exceptions import PageNotFoundException
from app.hotels.schemas import HotelSchemaForm, UpdateSchemaForm, ListHotelSchema, DetailHotelSchema, BaseHotelSchema
from app.hotels.services import HotelsService
from app.logging import logger

router = APIRouter(
    prefix='/hotels',
    tags=['Отели']
)


@router.get('/list', response_model=List[ListHotelSchema])
# @cache(expire=60) # TODO: Кэширование.
async def get_hotels():
    return await HotelsService.get_list_with_image_field()


@router.get('/detail/{hotel_id}', response_model=DetailHotelSchema)
async def get_hotel(hotel_id: int):
    hotel = await HotelsService.get_hotel_with_rooms_by_id(hotel_id)
    if not hotel:
        raise PageNotFoundException
    return hotel


@router.post('/create', response_model=BaseHotelSchema)
async def create_hotel(user=Depends(get_user_is_installer), data: HotelSchemaForm = Depends()):
    logger.info('Create hotel', extra={'user': {'id': user.id, 'email': user.email}})
    result_hotel = await HotelsService.create_object_with_image_field(**data.__dict__)
    hotel = result_hotel['Hotels']
    logger.info('Created hotel', extra={'hotel': {'id': hotel.id, 'title': hotel.title}})
    return result_hotel['Hotels']


@router.put('/update/{hotel_id}', response_model=BaseHotelSchema)
async def update_hotel(hotel_id: int, user=Depends(get_user_is_installer), data: UpdateSchemaForm = Depends()):
    logger.info('Update hotel', extra={'user': {'id': user.id, 'email': user.email}})
    hotel = await HotelsService.get_object_by_id(hotel_id)
    if not hotel:
        raise PageNotFoundException
    result_hotel = await HotelsService.update_object_with_image_field(obj=hotel, **data.__dict__)
    hotel = result_hotel['Hotels']
    logger.info('Updated hotel', extra={'hotel': {'id': hotel.id, 'title': hotel.title}})
    return hotel


@router.delete('/delete/{hotel_id}')
async def delete_hotel(hotel_id: int, user=Depends(get_user_is_installer)):
    await HotelsService.delete_object_by_id(hotel_id)
    logger.info('Deleted hotel', extra={'user': {'id': user.id, 'email': user.email}, 'hotel': {'id': hotel_id}})
    return {'detail': 'success'}
