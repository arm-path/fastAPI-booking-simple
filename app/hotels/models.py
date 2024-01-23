from typing import Optional, List

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.services.fields import pk, str_255


class Hotels(Base):
    __tablename__ = 'hotels'
    id: Mapped[pk]
    title: Mapped[str_255]
    location: Mapped[str_255]
    rooms_quantity: Mapped[int] = mapped_column(Integer, default=1)
    image_id: Mapped[Optional[int]] = mapped_column(ForeignKey('images.id', ondelete='SET NULL'), nullable=True)
    image: Mapped['Images'] = relationship('Images')
    rooms: Mapped[List['Rooms']] = relationship('Rooms', back_populates='hotel')

    def __str__(self):
        return f'<Hotels {self.id}: {self.title}>'
