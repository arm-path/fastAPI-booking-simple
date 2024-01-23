from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from app.exceptions import PageNotFoundException
from app.hotels.services import HotelsService
from app.hotels.routers import get_hotels, get_hotel

router = APIRouter(
    prefix='/pages',
    tags=['HTML страницы']
)
template = Jinja2Templates(directory='app/templates')


@router.get('/list-hotels')
def list_hotels_page(request: Request, hotels: get_hotels = Depends()):
    context = {
        'title': 'Список отелей',
        'hotels': hotels
    }
    return template.TemplateResponse(request, 'hotels/list_hotels.html', context=context)


@router.get('/detail-hotels/{hotel_id}')
def detail_hotels_page(request: Request, hotel_id: int, hotel: get_hotel = Depends()):
    context = {
        'title': hotel.title,
        'hotel': hotel
    }
    return template.TemplateResponse(request, 'hotels/detail_hotels.html', context=context)


@router.get('/create-hotels')
def create_hotels_page(request: Request):
    return template.TemplateResponse(request, 'hotels/create_hotels.html', context={'title': 'Создание отеля'})


@router.get('/update-hotels/{hotel_id}')
async def update_hotel_page(hotel_id: int, request: Request):
    hotel = await HotelsService.get_object_with_image_field(hotel_id)
    if not hotel:
        raise PageNotFoundException
    return template.TemplateResponse(request, 'hotels/update_hotels.html', context={'title': hotel.title, 'obj': hotel})
