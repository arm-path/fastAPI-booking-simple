import pytest

from app.hotels.services import HotelsService
from app.rooms.services import RoomService
from app.images.services import ImageService


@pytest.mark.parametrize('service, count_objects', [(HotelsService, 6), (RoomService, 9)])
async def test_get_list(service, count_objects):
    objects = await service.get_list()
    assert len(objects) == count_objects


@pytest.mark.parametrize('service, field, value, waiting_value', [(RoomService, 'hotel_id', 1, 2)])
async def test_get_list_by_filter(service, field, value, waiting_value):
    obj = await service.get_list(**{field: 1})
    assert len(obj) == waiting_value


@pytest.mark.parametrize('service, id, result', [(HotelsService, 1, True), (HotelsService, 10, False)])
async def test_get_object(service, id, result):
    hotel = await service.get_object(id=id)
    assert bool(hotel) == result
    if hotel:
        assert hotel.id == id


@pytest.mark.parametrize('service, data', [
    (HotelsService, {'title': 'hotel-1', 'location': 'address-1', 'rooms_quantity': 1}),
    (RoomService, {'title': 'room-1', 'hotel_id': 1})
])
async def test_create_object(service, data):
    await service.create_object(**data)
    objects = await service.get_list(**data)
    assert objects