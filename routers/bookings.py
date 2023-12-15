from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from database.database import get_db
from crud import booking_crud
from models.user import User as DBUser
from schemas.booking import BookingCreate
from security import oauth2
import datetime
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="static/html")

booking_router = APIRouter(prefix="/booking", tags=["Bookings"])

@booking_router.get("/", response_class=HTMLResponse)
def read_bookings(
    request: Request, 
    current_user: DBUser = Depends(oauth2.get_current_user_from_token), 
    db: Session = Depends(get_db)
    ):
    bookings = booking_crud.get_bookings(db, current_user.id)
    return templates.TemplateResponse("bookings.html",
                                      {
                                          "request": request,
                                          "bookings": bookings,
                                          "current_date_time": datetime.datetime.now()
                                      },
                                      status_code=status.HTTP_200_OK
    )


@booking_router.get("/search/", response_class=HTMLResponse)
def read_booking(
    request: Request,
    id: int, 
    db: Session = Depends(get_db), 
    current_user: DBUser = Depends(oauth2.get_current_user_from_token)
    ):
    booking = booking_crud.get_booking(db, id, current_user.id)
    if not booking:
        return templates.TemplateResponse(
            "bookings.html",
            {
                "request": request,
                "no_booking_found": True,
                "id": id
            }
        )
    return templates.TemplateResponse(
        "bookings.html",
        {
            "request": request,
            "bookings": [booking],
            "current_date_time": datetime.datetime.now()
        }
    )


@booking_router.post("/new/", response_class=HTMLResponse)
def create_booking(
    request: Request, 
    booking: BookingCreate = Depends(BookingCreate.as_form), 
    db: Session = Depends(get_db), 
    current_user: DBUser = Depends(oauth2.get_current_user_from_token)
    ):

    booking_crud.create_user_booking(db, booking, current_user.id)
    return RedirectResponse(
        url="/booking",
        status_code=status.HTTP_303_SEE_OTHER
    )


@booking_router.get("/new/", response_class=HTMLResponse)
def send_form(
    request: Request, 
    current_user: DBUser = Depends(oauth2.get_current_user_from_token)
    ):
    min_date_time = datetime.datetime.now()
    min_date = str(min_date_time.date())
    min_time = min_date_time.time()
    min_time = f"{min_time.hour:02}:{min_time.minute:02}"

    return templates.TemplateResponse(
        "create_booking.html",
        {
            "request": request,
            "url": "/booking/new/",
            "min_date": min_date,
            "min_time": min_time
        }
    )


@booking_router.get("/update/{id}", response_class=HTMLResponse)
def send_update_form(
    request: Request,
    id: int,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(oauth2.get_current_user_from_token)
    ):
    booking = booking_crud.get_booking(db, id, current_user.id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can't change the booking with this ID"
        )
    dep_date_time: datetime.datetime = booking.dep_date_time
    if dep_date_time < datetime.datetime.now():
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="You can't change the booking with this ID"
        )
    dep_date = dep_date_time.date()
    dep_time = dep_date_time.time()
    dep_date_time = f"{dep_date}T{dep_time.hour:02}:{dep_time.minute:02}"
    min_date_time = datetime.datetime.now()
    duration = f"{booking.duration.hour:02}:{booking.duration.minute:02}"

    return templates.TemplateResponse(
        "update_booking.html",
        {
            "request": request,
            "id": booking.id,
            "origin": booking.origin,
            "destination": booking.destination,
            "dep_date_time": dep_date_time,
            "duration": duration,
            "min_date": min_date_time.date(),
            "min_time": f"{min_date_time.time().hour:02}:{min_date_time.time().minute:02}"
        },
        status_code=status.HTTP_200_OK
    )



@booking_router.post("/update/{id}", response_class=HTMLResponse)
def update_booking(
    id: int, 
    booking: BookingCreate = Depends(BookingCreate.as_form), 
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(oauth2.get_current_user_from_token)
    ):
    updated = booking_crud.update_booking(db, booking, id, current_user.id)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    return RedirectResponse(
        "/booking/",
        status_code=status.HTTP_302_FOUND
    )


@booking_router.get("/delete/{id}", response_class=RedirectResponse)
def delete_booking(id: int, db: Session = Depends(get_db), current_user: DBUser = Depends(oauth2.get_current_user_from_token)):
    deleted = booking_crud.delete_booking(db, id, current_user.id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    return RedirectResponse(
        "/booking",
        status_code=status.HTTP_302_FOUND
    )
