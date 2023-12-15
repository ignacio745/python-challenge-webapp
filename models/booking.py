from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Time
from sqlalchemy.orm import relationship
from database.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    origin = Column(String)
    destination = Column(String)
    dep_date_time = Column(DateTime)
    duration = Column(Time)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    owner = relationship("User", back_populates="bookings")