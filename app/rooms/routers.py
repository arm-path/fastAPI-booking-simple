from typing import List

from fastapi import APIRouter, Depends

from app.authentication.services import get_user_is_installer
from app.exceptions import PageNotFoundException, NotFoundHotelException
from app.logging import logger
from app.rooms.schemas import RoomListSchema, RoomDetailSchema, CreateRoomSchemaForm, UpdateRoomSchemaForm
from app.rooms.services import RoomService, get_log_fields_room

router = APIRouter(
    prefix='/rooms',
    tags=['Комнаты отелей']
)


@router.get('/list/{hotel_id}')
async def get_rooms(hotel_id: int) -> List[RoomListSchema]:
    rooms = await RoomService.get_list_with_image_field(hotel_id=hotel_id)
    return rooms


@router.get('/detail/{room_id}')
async def get_room(room_id: int) -> RoomDetailSchema:
    room = await RoomService.get_object_with_image_field(room_id)
    if not room:
        raise PageNotFoundException
    return room


@router.post('/create')
async def create_room(user=Depends(get_user_is_installer), data: CreateRoomSchemaForm = Depends()):
    logger.info('Create room', extra={'user': {'id': user.id, 'email': user.email}})
    hotel = await RoomService.get_object_by_id(data.hotel_id)
    if not hotel:
        raise NotFoundHotelException
    room = await RoomService.create_object_with_image_field(**data.__dict__)
    logger.info('Created room', extra={'room': get_log_fields_room(room['Rooms'])})
    return room['Rooms']


@router.put('/update/{room_id}')
async def update_room(room_id: int, user=Depends(get_user_is_installer), data: UpdateRoomSchemaForm = Depends()):
    logger.info('Update room', extra={'user': {'id': user.id, 'email': user.email}})
    room = await RoomService.get_object_by_id(id=room_id)
    if not room:
        raise PageNotFoundException
    result_room = await RoomService.update_object_with_image_field(obj=room, **data.__dict__)

    logger.info('Updated room', extra={'room': {'id': result_room['Rooms'].id, 'initial': get_log_fields_room(room),
                                                'changed': get_log_fields_room(result_room['Rooms'])}})
    return result_room


@router.delete('/delete/{room_id}')
async def delete_room(room_id: int, user=Depends(get_user_is_installer)):
    await RoomService.delete_object_by_id(room_id)
    logger.info('Deleted room', extra={'user': {'id': user.id, 'email': user.email}, 'room': {'id': room_id}})
    return {'detail': 'success'}
