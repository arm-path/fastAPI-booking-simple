from typing import Optional

from sqlalchemy import Integer, String, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.hotels.models import Hotels
from app.services.fields import pk, str_255


class Rooms(Base):
    __tablename__ = 'rooms'
    id: Mapped[pk]
    title: Mapped[str_255]
    hotel_id: Mapped[int] = mapped_column(Integer, ForeignKey('hotels.id', ondelete='CASCADE'))
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    price: Mapped[int] = mapped_column(Integer, default=0)
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    image_id: Mapped[Optional[int]] = mapped_column(ForeignKey('images.id', ondelete='SET NULL'), nullable=True)
    hotel: Mapped['Hotels'] = relationship('Hotels', back_populates='rooms')
    image: Mapped['Images'] = relationship('Images', back_populates='rooms')
    bookings = relationship('Bookings', back_populates='room')

    def __str__(self):
        return f'<Rooms {self.id}: {self.title}>'
