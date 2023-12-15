from typing import Optional, Annotated

from fastapi import Form
from pydantic import BaseModel, EmailStr

from .booking import Booking


class UserBase(BaseModel):
    email: EmailStr


class User(UserBase):
    bookings: list[Booking] = []
    
    class Config:
        orm_mode = True


class UserCreate(UserBase):
    name: str
    password: str

    @classmethod
    def as_form(
        cls,
        email: Annotated[EmailStr, Form()],
        name: Annotated[str, Form()],
        password: Annotated[str, Form()]
    ):
        return cls(email=email, name=name, password=password)


class UserSignIn(UserBase):
    password: str