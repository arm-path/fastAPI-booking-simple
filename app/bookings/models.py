from datetime import date

from sqlalchemy import Integer, ForeignKey, Date, Computed
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.services.fields import pk, auto_now_add, auto_now


class Bookings(Base):
    __tablename__ = 'bookings'
    id: Mapped[pk]
    room_id: Mapped[int] = mapped_column(Integer, ForeignKey('rooms.id', ondelete='CASCADE'))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    date_from: Mapped[date] = mapped_column(Date, nullable=False)
    date_to: Mapped[date] = mapped_column(Date, nullable=False)
    price: Mapped[int] = mapped_column(Integer, default=0)
    total_cost: Mapped[int] = mapped_column(Integer, Computed('(date_to - date_from) * price'))
    total_days: Mapped[int] = mapped_column(Integer, Computed('date_to - date_from'))
    created_at: Mapped[auto_now_add]
    updated_at: Mapped[auto_now]

    user = relationship('Users', back_populates='bookings')
    room = relationship('Rooms', back_populates='bookings')

    def __str__(self):
        return f'<Bookings {self.id}: {self.date_from}-{self.date_to}'
