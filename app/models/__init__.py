from app.database import Base
from .user import User, Patient, Doctor, Admin, Secretary
from .clinic import Clinic, clinic_doctors, clinic_secretaries
from .appointment import Appointment

__all__ = [
    "Base",
    "User",
    "Patient",
    "Doctor",
    "Admin",
    "Secretary",
    "Clinic",
    "clinic_doctors",
    "clinic_secretaries",
    "Appointment",
]
