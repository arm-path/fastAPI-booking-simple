from typing import Optional

from sqlalchemy import Boolean, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.services.fields import pk, str_255


class Users(Base):
    __tablename__ = 'users'
    id: Mapped[pk]
    email: Mapped[str_255]
    hashed_password: Mapped[str_255]
    email_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=text('False'))
    installer: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=text('False'))

    bookings = relationship('Bookings', back_populates='user')

    def __str__(self):
        return f'<Users {self.id}: {self.email}'
