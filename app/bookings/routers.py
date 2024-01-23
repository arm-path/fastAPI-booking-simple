from typing import List

from fastapi import APIRouter, Depends

from app.authentication.services import get_current_user
from app.bookings.schemas import ListBookingSchema, CreateBookingSchema
from app.bookings.services import BookingService
from app.exceptions import NoRoomsAvailableException, NotFoundRoomException, NotFoundBookingException
from app.logging import logger
from app.rooms.services import RoomService
from app.users.schemas import UserSchema

router = APIRouter(
    prefix='/booking',
    tags=['Бронирования']
)


@router.get('/')
async def get_bookings(user: UserSchema = Depends(get_current_user)) -> List[ListBookingSchema]:
    return await BookingService.get_list(user_id=user.id)


@router.post('/create')
async def create_booking(data: CreateBookingSchema, user: UserSchema = Depends(get_current_user)):
    room = await RoomService.get_object_by_id(data.room_id)
    if not room:
        raise NotFoundRoomException
    available_rooms = await BookingService.check_available_rooms(data.room_id, data.date_from, data.date_to)
    if not available_rooms.remainder > 0:
        raise NoRoomsAvailableException
    booking = await BookingService.create_object(
        room_id=data.room_id,
        user_id=user.id,
        date_from=data.date_from,
        date_to=data.date_to,
        price=available_rooms.price
    )
    logger.info('Booking created', extra={'id': booking.id, 'user_id': user.id, 'room_id': data.room_id,
                                          'from': data.date_from, 'to': data.date_to})
    return {'detail': ' Bookings created success!', 'id': booking.id}


@router.delete('/delete/{booking_id}')
async def delete_booking(booking_id: int, user: UserSchema = Depends(get_current_user)):
    booking = await BookingService.get_object_by_id(booking_id)
    if not booking:
        raise NotFoundBookingException
    if booking.user_id != user.id:
        raise NotFoundBookingException
    await BookingService.delete_object_by_id(booking_id)
    logger.info('Booking deleted', extra={'user_id': user.id, 'booking_id': booking.id})
    return {'detail': 'Booking deleted success'}
