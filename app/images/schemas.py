from pydantic import BaseModel


class ImageSchema(BaseModel):
    id: int
    title: str
    upload_to: str
