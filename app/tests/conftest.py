import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy import text
from fastapi.testclient import TestClient

from app.main import app as app_for_test
from app.database import engine
from app.bookings.models import Bookings
from app.database import Base
from app.hotels.models import Hotels
from app.rooms.models import Rooms
from app.images.models import Images
from app.users.models import Users


@pytest.fixture(scope='session', autouse=True)
async def preparation():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        database_name = [Users.__tablename__, Hotels.__tablename__, Rooms.__tablename__, Bookings.__tablename__]
        for name in database_name:
            with open(f'app/tests/preparation_data/test_{name}.sql', encoding='utf-8') as file:
                sql_text = file.read()
                await conn.execute(text(sql_text))
        await conn.commit()


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app_for_test)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app_for_test, base_url="http://test") as ac:
        yield ac
