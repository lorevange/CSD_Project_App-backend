from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, LargeBinary, String, Text, and_
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.model_review import Review


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
    reviews_authored = relationship("Review", back_populates="author", foreign_keys="Review.author_id")


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
    information = Column(Text, nullable=True)

    user = relationship("User", back_populates="doctor")
    appointments = relationship("Appointment", back_populates="doctor")
    days = relationship("Day", back_populates="doctor")
    services = relationship("DoctorService", back_populates="doctor", cascade="all, delete-orphan")
    reviews = relationship(
        "Review",
        back_populates="doctor",
        primaryjoin="and_(Doctor.id == Review.doctor_id, Review.deleted_at.is_(None))",
    )
    photo = association_proxy("user", "photo")
    identity_number = association_proxy("user", "identity_number")
