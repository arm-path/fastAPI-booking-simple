from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin

from app.database import engine
from app.authentication.routers import router as security_router
from app.bookings.routers import router as booking_router
from app.hotels.routers import router as hotel_router
from app.images.routers import router as image_router
from app.mail.routers import router as mail_router
from app.pages.routers import router as page_router
from app.rooms.routers import router as room_router
from app.users.routers import router as user_router
from app.admin.securiry import authentication_backend
from app.admin.admin import HotelsAdmin, RoomsAdmin, UsersAdmin, BookingsAdmin

app = FastAPI()

app.include_router(security_router)
app.include_router(user_router)
app.include_router(hotel_router)
app.include_router(room_router)
app.include_router(booking_router)
app.include_router(image_router)
app.include_router(mail_router)
app.include_router(page_router)

app.mount('/static', StaticFiles(directory='app/static'), 'static')

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)

# @app.on_event("startup")
# async def startup():
#     redis = aioredis.from_url("redis://localhost")
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
