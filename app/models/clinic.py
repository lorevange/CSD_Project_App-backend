from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.database import Base

clinic_doctors = Table(
    "clinic_doctors",
    Base.metadata,
    Column("clinic_id", Integer, ForeignKey("Clinic.id"), primary_key=True),
    Column("doctor_id", String, ForeignKey("Doctor.identity_number"), primary_key=True),
)

clinic_secretaries = Table(
    "clinic_secretaries",
    Base.metadata,
    Column("clinic_id", Integer, ForeignKey("Clinic.id"), primary_key=True),
    Column("secretary_id", String, ForeignKey("Secretary.identity_number"), primary_key=True),
)


class Clinic(Base):
    __tablename__ = "Clinic"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    cap = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)

    doctors = relationship("Doctor", secondary=clinic_doctors, back_populates="clinics")
    secretaries = relationship("Secretary", secondary=clinic_secretaries, back_populates="clinics")
    appointments = relationship("Appointment", back_populates="clinic")
