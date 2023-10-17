from pydantic import BaseModel
from datetime import date


class ContactModel(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    birthday: date


class ResponseContact(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    birthday: date

    class Config:
        from_attributes = True
