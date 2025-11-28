from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "User"

    identity_number = Column(String, primary_key=True, index=True, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    profile = Column(String, nullable=False)  # "patient", "doctor", "admin", "secretary"
    email = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)

    patient = relationship("Patient", back_populates="user", uselist=False)
    doctor = relationship("Doctor", back_populates="user", uselist=False)
    admin = relationship("Admin", back_populates="user", uselist=False)
    secretary = relationship("Secretary", back_populates="user", uselist=False)

    @property
    def id(self) -> str:
        return self.identity_number


class Patient(Base):
    __tablename__ = "Patient"

    identity_number = Column(String, ForeignKey("User.identity_number"), primary_key=True)

    user = relationship("User", back_populates="patient")
    appointments = relationship("Appointment", back_populates="patient")


class Doctor(Base):
    __tablename__ = "Doctor"

    identity_number = Column(String, ForeignKey("User.identity_number"), primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    license_number = Column(String, nullable=False)
    specialization = Column(String, nullable=False)

    user = relationship("User", back_populates="doctor")
    clinics = relationship("Clinic", secondary="clinic_doctors", back_populates="doctors")
    appointments = relationship("Appointment", back_populates="doctor")


class Admin(Base):
    __tablename__ = "Admin"

    identity_number = Column(String, ForeignKey("User.identity_number"), primary_key=True)
    is_superadmin = Column(Boolean, default=False)

    user = relationship("User", back_populates="admin")


class Secretary(Base):
    __tablename__ = "Secretary"

    identity_number = Column(String, ForeignKey("User.identity_number"), primary_key=True)

    user = relationship("User", back_populates="secretary")
    clinics = relationship("Clinic", secondary="clinic_secretaries", back_populates="secretaries")
