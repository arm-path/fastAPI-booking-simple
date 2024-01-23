from pydantic import BaseModel, EmailStr


class MailSchema(BaseModel):
    to: EmailStr
    subject: str
    text: str
