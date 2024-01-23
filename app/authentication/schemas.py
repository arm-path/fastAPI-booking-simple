from pydantic import BaseModel, EmailStr, field_validator
from pydantic_core.core_schema import ValidationInfo

from app.exceptions import PasswordMismatchException


class RegistrationUserSchema(BaseModel):
    email: EmailStr
    password_1: str
    password_2: str

    @field_validator('password_2')
    def validate_password(cls, value: str, values: ValidationInfo):
        if values.data['password_1'] != value:
            raise PasswordMismatchException

        return value

    class Config:
        orm_mode = True


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
