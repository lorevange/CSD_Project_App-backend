from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Appointment(Base):
    __tablename__ = "Appointment"

    id = Column(Integer, primary_key=True, autoincrement=True)
    doctor_id = Column(String, ForeignKey("Doctor.identity_number"), nullable=False)
    datetime = Column(DateTime, nullable=False)
    examination_type = Column(String, nullable=False)
    notes = Column(Text, nullable=True)
    status = Column(String, nullable=False, default="scheduled")

    doctor = relationship("Doctor", back_populates="appointments")
