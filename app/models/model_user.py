from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, LargeBinary, String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    identity_number = Column(String, nullable=False, unique=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    profile = Column(String, nullable=False)  # allowed: "doctor"
    email = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    password = Column(String, nullable=True)
    photo = Column(LargeBinary, nullable=True)

    doctor = relationship("Doctor", back_populates="user", uselist=False)
    appointments = relationship("Appointment", back_populates="user", foreign_keys="Appointment.user_id")


class Doctor(Base):
    __tablename__ = "Doctor"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey("User.id"), nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    license_number = Column(String, nullable=False)
    specialization = Column(String, nullable=False)
    city = Column(String, nullable=True)
    address = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    user = relationship("User", back_populates="doctor")
    appointments = relationship("Appointment", back_populates="doctor")
    days = relationship("Day", back_populates="doctor")
    services = relationship("DoctorService", back_populates="doctor", cascade="all, delete-orphan")
    photo = association_proxy("user", "photo")
    identity_number = association_proxy("user", "identity_number")
