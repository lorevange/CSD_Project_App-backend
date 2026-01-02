from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class DoctorService(Base):
    __tablename__ = "DoctorService"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    doctor_id = Column(Integer, ForeignKey("Doctor.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    doctor = relationship("Doctor", back_populates="services")
    appointments = relationship("Appointment", back_populates="doctor_service")
