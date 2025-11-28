from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

# ===========================
# Base User
# ===========================
class UserBase(BaseModel):
    first_name: str
    last_name: str
    identity_number: str
    email: str
    phone_number: Optional[str] = None


# ===========================
# Patient
# ===========================
class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    identity_number: str
    email: str
    phone_number: Optional[str] = None
    prova: Optional[str] = None


class PatientOut(BaseModel):
    prova: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


# ===========================
# Doctor
# ===========================
class DoctorCreate(BaseModel):
    first_name: str
    last_name: str
    identity_number: str
    email: str
    phone_number: Optional[str] = None
    license_number: str
    specialization: str


class DoctorOut(BaseModel):
    license_number: str
    specialization: str
    model_config = ConfigDict(from_attributes=True)


# ===========================
# Admin
# ===========================
class AdminCreate(UserBase):
    first_name: str
    last_name: str
    identity_number: str
    email: str
    phone_number: Optional[str] = None
    is_superadmin: Optional[bool] = False


class AdminOut(BaseModel):
    is_superadmin: bool
    model_config = ConfigDict(from_attributes=True)


# ===========================
# Secretary
# ===========================
class SecretaryCreate(UserBase):
    first_name: str
    last_name: str
    identity_number: str
    email: str
    phone_number: Optional[str] = None
    prova: Optional[str] = None


class SecretaryOut(BaseModel):
    prova: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


# ===========================
# User output (con profilo)
# ===========================
class UserOut(UserBase):
    id: str
    profile: str
    patient: Optional[PatientOut] = None
    doctor: Optional[DoctorOut] = None
    admin: Optional[AdminOut] = None
    secretary: Optional[SecretaryOut] = None

    model_config = ConfigDict(from_attributes=True)


# Clinic
# ===========================
class ClinicBase(BaseModel):
    name: str
    address: str
    city: str
    cap: str
    phone: str
    email: str

class ClinicCreate(ClinicBase):
    pass  # for now nothing to add

class ClinicOut(ClinicBase):
    id: int
    doctors: Optional[List[DoctorOut]] = []      # lista di identity_number dei dottori
    secretaries: Optional[List[SecretaryOut]] = []  # lista di identity_number delle segretarie

    model_config = ConfigDict(from_attributes=True)


class AppointmentCreate(BaseModel):
    doctor_id: str
    patient_id: str
    clinic_id: int
    datetime: datetime
    examination_type: str
    notes: Optional[str] = None
    status: Optional[str] = "scheduled"



class AppointmentOut(BaseModel):
    id: int
    doctor_id: str
    patient_id: str
    clinic_id: int
    datetime: datetime
    examination_type: str
    notes: Optional[str] = None
    status: str

    model_config = ConfigDict(from_attributes=True)