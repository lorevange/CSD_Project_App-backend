from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Time
from sqlalchemy.orm import relationship

from app.database import Base


class Day(Base):
    __tablename__ = "Day"

    id = Column(Integer, primary_key=True, autoincrement=True)
    week_day = Column(Integer, nullable=False)  # sunday=0 ... saturday=6
    opening = Column(Time, nullable=False)
    closing = Column(Time, nullable=False)
    is_closed = Column(Boolean, nullable=False)
    doctor_id = Column(String, ForeignKey("Doctor.identity_number"), nullable=False)

    doctor = relationship("Doctor", back_populates="days")
