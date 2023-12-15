from models.booking import Booking as DBBooking
from schemas.booking import Booking
from sqlalchemy.orm import Session


def get_bookings(db: Session, user_id: int):
    return db.query(DBBooking).filter(DBBooking.owner_id == user_id).order_by(DBBooking.id).all()


def get_booking(db: Session, id: int, user_id: int):
    booking = db.query(DBBooking).filter(DBBooking.id == id).first()
    if not booking:
        return False
    if booking.owner_id != user_id:
        return False
    return booking


def create_user_booking(db: Session, booking: Booking, user_id: int):
    db_booking = DBBooking(**booking.dict(), owner_id=user_id)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


def update_booking(db: Session, booking: Booking, id: int, user_id: int):
    booking_to_update = db.query(DBBooking).filter(DBBooking.id == id).first()
    if not booking_to_update:
        return False
    if booking_to_update.owner_id != user_id:
        return False
    des_booking = booking.dict(exclude_unset=True).items()
    for k, v in des_booking:
        setattr(booking_to_update, k, v)
    db.commit()
    db.refresh(booking_to_update)
    return booking_to_update


def delete_booking(db: Session, id: int, user_id: int):
    booking_to_delete = db.query(DBBooking).filter(DBBooking.id == id).first()
    if not booking_to_delete:
        return False
    if booking_to_delete.owner_id != user_id:
        return False
    db.delete(booking_to_delete)
    db.commit()
    return True