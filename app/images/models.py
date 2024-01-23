from typing import List

from sqlalchemy.orm import Mapped, relationship

from app.database import Base
from app.services.fields import pk, str_255


class Images(Base):
    __tablename__ = 'images'
    id: Mapped[pk]
    title: Mapped[str_255]
    upload_to: Mapped[str_255]
    hotels: Mapped[List['Hotels']] = relationship('Hotels', back_populates='image')
    rooms: Mapped[List['Rooms']] = relationship('Rooms', back_populates='image')

    def __str__(self):
        return f'<Images {self.id}: {self.title}>'
