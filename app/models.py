from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean, Table
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
    appointments = relationship("Appointment", back_populates="patient")

class Doctor(Base):
    __tablename__ = "Doctor"

    identity_number = Column(String, ForeignKey("User.identity_number"), primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    license_number = Column(String, nullable=False)
    specialization = Column(String, nullable=False)

    user = relationship("User", back_populates="doctor")
     # Relazione many-to-many con Clinic
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
    
    prova = Column(String, nullable=True)
    user = relationship("User", back_populates="secretary")
     # Relazione many-to-many con Clinic
    clinics = relationship("Clinic", secondary="clinic_secretaries", back_populates="secretaries")


# Associazione Many-to-Many Clinic <-> Doctor
clinic_doctors = Table(
    "clinic_doctors",
    Base.metadata,
    Column("clinic_id", Integer, ForeignKey("Clinic.id"), primary_key=True),
    Column("doctor_id", String, ForeignKey("Doctor.identity_number"), primary_key=True),
)

# Associazione Many-to-Many Clinic <-> Secretary
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

    # Relazioni many-to-many
    doctors = relationship("Doctor", secondary=clinic_doctors, back_populates="clinics")
    secretaries = relationship("Secretary", secondary=clinic_secretaries, back_populates="clinics")
    appointments = relationship("Appointment", back_populates="clinic")

class Appointment(Base):
    __tablename__ = "Appointment"

    id = Column(Integer, primary_key=True, autoincrement=True)
    doctor_id = Column(String, ForeignKey("Doctor.identity_number"), nullable=False)
    patient_id = Column(String, ForeignKey("Patient.identity_number"), nullable=False)
    clinic_id = Column(Integer, ForeignKey("Clinic.id"), nullable=False)
    datetime = Column(DateTime, nullable=False)
    examination_type = Column(String, nullable=False)
    notes = Column(Text, nullable=True)
    status = Column(String, nullable=False, default="scheduled")  # nuovo campo status

    # Relazioni
    doctor = relationship("Doctor", back_populates="appointments")
    patient = relationship("Patient", back_populates="appointments")
    clinic = relationship("Clinic", back_populates="appointments")
