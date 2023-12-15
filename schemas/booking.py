import datetime
from typing import Optional, Annotated
from pydantic import BaseModel, validator
from fastapi import Form


class Booking(BaseModel):
    origin: str
    destination: str
    dep_date_time: datetime.datetime
    duration: datetime.time

    class Config:
        orm_mode = True


class BookingCreate(BaseModel):
    origin: str
    destination: str
    dep_date_time: datetime.datetime
    duration: datetime.time

    @validator("dep_date_time")
    def ensure_datetime_range(cls, value):
        if value < datetime.datetime.now():
            raise ValueError("Invalid date and time")
        return value
    
    @classmethod
    def as_form(
        cls,
        origin: Annotated[str, Form()],
        destination: Annotated[str, Form()],
        dep_date_time: Annotated[datetime.datetime, Form()],
        duration: Annotated[datetime.time, Form()]
    ):
        date = dep_date_time.date()
        time = dep_date_time.time()
        time = datetime.time(time.hour, time.minute)
        dep_date_time_without_seconds = datetime.datetime.combine(date, time)
        return cls(origin=origin, destination=destination, dep_date_time=dep_date_time_without_seconds, duration=duration)

    class Config:
        orm_mode = True


class BookingResponse(Booking):
    id: int