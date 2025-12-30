from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import timedelta

from app.database import Base


class Appointment(Base):
    __tablename__ = "Appointment"
    __table_args__ = (
        UniqueConstraint("doctor_id", "start_datetime", name="uq_doctor_slot"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    doctor_id = Column(String, ForeignKey("Doctor.identity_number"), nullable=False)
    user_id = Column(String, ForeignKey("User.identity_number"), nullable=False)
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)
    examination_type = Column(String, nullable=False)
    notes = Column(Text, nullable=True)
    status = Column(String, nullable=False, default="scheduled")

    doctor = relationship("Doctor", back_populates="appointments")
    user = relationship("User", back_populates="appointments")

    @staticmethod
    def default_duration() -> timedelta:
        return timedelta(minutes=30)
