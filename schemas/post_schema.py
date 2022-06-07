import datetime

from pydantic import BaseModel, ValidationError, validator, EmailStr


class Post(BaseModel):
    id: int
    title: str
    text: str
    created_at: datetime.datetime
