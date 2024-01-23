from app.rooms.models import Rooms
from app.services.database import DatabaseService


class RoomService(DatabaseService):
    model = Rooms


def get_log_fields_room(room):
    return {'id': room.id, 'title': room.title, 'hotel_id': room.hotel_id, 'description': room.description,
            'price': room.price, 'quantity': room.quantity, 'image_id': room.image_id}
