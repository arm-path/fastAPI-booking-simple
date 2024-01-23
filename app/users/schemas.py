from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    id: int
    email: EmailStr
    installer: bool

    class Config:
        orm_mode = True
