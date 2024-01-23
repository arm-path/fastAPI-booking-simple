from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.settings import settings

DATABASE_URL = settings.TEST_DATABASE_URL if settings.MODE == 'TEST' else settings.DATABASE_URL
engine = create_async_engine(DATABASE_URL, poolclass=NullPool if settings.MODE == 'TEST' else None)
session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
