from sqladmin import ModelView

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.rooms.models import Rooms
from app.users.models import Users


class HotelsAdmin(ModelView, model=Hotels):
    column_list = ['title', 'location', 'image', 'rooms_quantity']
    column_searchable_list = ['title']
    column_details_list = ['id', 'title', 'location', 'image', 'rooms']
    page_size = 7

    can_export = True

    name = 'Hotel'
    name_plural = 'Hotels'
    icon = 'fa-solid fa-hotel'


class RoomsAdmin(ModelView, model=Rooms):
    column_list = ['title', 'hotel', 'price', 'quantity', 'image']
    column_searchable_list = ['title']
    column_details_list = ['id', 'title', 'hotel', 'description', 'price', 'quantity', 'image']
    page_size = 25

    name = 'Room'
    name_plural = 'Rooms'
    icon = 'fa-solid fa-bed'


class UsersAdmin(ModelView, model=Users):
    column_list = ['email', 'email_verified', 'installer']
    column_details_list = ['id', 'email', 'email_verified', 'installer', 'bookings']
    form_columns = ['id', 'email', 'email_verified', 'installer']
    form_widget_args = dict(email=dict(readonly=True))

    can_create = False
    can_export = False
    can_delete = False

    name = 'User'
    name_plural = 'Users'
    icon = 'fa-solid fa-users'


class BookingsAdmin(ModelView, model=Bookings):
    column_list = ['id', 'room', 'user', 'date_from', 'date_to']
    column_details_list = ['id', 'room', 'user', 'date_from', 'date_to', 'price', 'total_cost', 'total_days',
                           'created_at', 'updated_at']

    can_create = False

    name = 'Booking'
    name_plural = 'Bookings'
    icon = 'fa-solid fa-utensils'
