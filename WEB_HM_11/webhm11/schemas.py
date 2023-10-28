from pydantic import BaseModel, Field, EmailStr
from datetime import date
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType


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


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    avatar: str

    class Config:
        form_attributes = True


class ResponseUser(BaseModel):
    user: UserDb
    detatil: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class EmailSchema(BaseModel):
    email: EmailStr


class ResponseModel(BaseModel):
    message: str
    avatar_url: str


class RequestEmail(BaseModel):
    email: EmailStr

    class Config:
        from_attributes = True
