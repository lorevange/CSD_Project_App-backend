from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, Numeric, String, Text, text
from sqlalchemy.orm import relationship
from datetime import timedelta

from app.database import Base


class Appointment(Base):
    __tablename__ = "Appointment"
    __table_args__ = (
        Index(
            "uq_doctor_slot_scheduled",
            "doctor_id",
            "start_datetime",
            unique=True,
            sqlite_where=text("status = 'scheduled'"),
            postgresql_where=text("status = 'scheduled'"),
        ),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    doctor_id = Column(Integer, ForeignKey("Doctor.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("User.id"), nullable=False)
    doctor_service_id = Column(Integer, ForeignKey("DoctorService.id"), nullable=False)
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)
    examination_type = Column(String, nullable=False)
    price_at_booking = Column(Numeric(10, 2), nullable=False)
    notes = Column(Text, nullable=True)
    status = Column(String, nullable=False, default="scheduled")

    doctor = relationship("Doctor", back_populates="appointments")
    doctor_service = relationship("DoctorService", back_populates="appointments")
    user = relationship("User", back_populates="appointments")

    @staticmethod
    def default_duration() -> timedelta:
        return timedelta(minutes=30)
