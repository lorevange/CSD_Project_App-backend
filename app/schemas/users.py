from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    first_name: str
    last_name: str
    identity_number: str
    email: str
    phone_number: Optional[str] = None


class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    identity_number: str
    email: str
    phone_number: Optional[str] = None


class PatientOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class DoctorCreate(BaseModel):
    first_name: str
    last_name: str
    identity_number: str
    email: str
    phone_number: Optional[str] = None
    license_number: str
    specialization: str


class DoctorOut(BaseModel):
    identity_number: str
    first_name: str
    last_name: str
    license_number: str
    specialization: str
    model_config = ConfigDict(from_attributes=True)


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


class SecretaryCreate(UserBase):
    first_name: str
    last_name: str
    identity_number: str
    email: str
    phone_number: Optional[str] = None


class SecretaryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserOut(UserBase):
    id: str
    profile: str
    patient: Optional[PatientOut] = None
    doctor: Optional[DoctorOut] = None
    admin: Optional[AdminOut] = None
    secretary: Optional[SecretaryOut] = None

    model_config = ConfigDict(from_attributes=True)
