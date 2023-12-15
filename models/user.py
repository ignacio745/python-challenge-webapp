from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    name = Column(String)
    hashed_password = Column(String)

    bookings = relationship("Booking", back_populates="owner", cascade="all, delete")

