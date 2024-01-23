from pydantic import BaseModel, field_validator
from datetime import date

from app.exceptions import ErrorInBookingDateException


class CreateBookingSchema(BaseModel):
    room_id: int
    date_from: date
    date_to: date

    @field_validator('date_to')
    def validate_date_to(cls, value: str, values):
        if values.data['date_from'] >= value:
            raise ErrorInBookingDateException
        return value


class ListBookingSchema(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int

    class Config:
        orm_mode = True
