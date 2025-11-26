from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "User"

    identity_number = Column(String, primary_key=True, index=True, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    profile = Column(String, nullable=False)  # "patient", "doctor", "admin", "secretary"
    email = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)

    # Relazioni one-to-one con le tabelle specifiche
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
    prova = Column(String, nullable=True)

    user = relationship("User", back_populates="patient")


class Doctor(Base):
    __tablename__ = "Doctor"

    identity_number = Column(String, ForeignKey("User.identity_number"), primary_key=True)
    license_number = Column(String, nullable=False)
    specialization = Column(String, nullable=False)

    user = relationship("User", back_populates="doctor")


# =========================
# Nuove tabelle
# =========================
class Admin(Base):
    __tablename__ = "Admin"

    identity_number = Column(String, ForeignKey("User.identity_number"), primary_key=True)
    is_superadmin = Column(Boolean, default=False)

    user = relationship("User", back_populates="admin")


class Secretary(Base):
    __tablename__ = "Secretary"

    identity_number = Column(String, ForeignKey("User.identity_number"), primary_key=True)
    # working_clinic sarà aggiunto successivamente per la relazione many-to-many
    prova = Column(String, nullable=True)
    user = relationship("User", back_populates="secretary")
