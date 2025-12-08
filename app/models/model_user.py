from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "User"

    identity_number = Column(String, primary_key=True, index=True, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    profile = Column(String, nullable=False)  # allowed: "doctor"
    email = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    password = Column(String, nullable=True)

    doctor = relationship("Doctor", back_populates="user", uselist=False)

    @property
    def id(self) -> str:
        return self.identity_number


class Doctor(Base):
    __tablename__ = "Doctor"

    identity_number = Column(String, ForeignKey("User.identity_number"), primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    license_number = Column(String, nullable=False)
    specialization = Column(String, nullable=False)

    user = relationship("User", back_populates="doctor")
    appointments = relationship("Appointment", back_populates="doctor")
    days = relationship("Day", back_populates="doctor")
