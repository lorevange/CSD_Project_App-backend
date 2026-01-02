from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.schema_appointments import AppointmentOut
from app.schemas.schema_days import DayOut
from app.schemas.schema_doctor_services import DoctorServiceOut


class UserCreateBase(BaseModel):
    first_name: str
    last_name: str
    identity_number: str
    email: str
    phone_number: Optional[str] = None
    password: str
    photo: Optional[bytes] = None


class UserBase(BaseModel):
    first_name: str
    last_name: str
    identity_number: str
    email: str
    phone_number: Optional[str] = None
    photo: Optional[bytes] = None

class UserEdit(BaseModel):
    first_name: str
    last_name: str
    identity_number: str
    photo: Optional[bytes] = None

class DoctorCreate(UserCreateBase):
    license_number: str
    specialization: str
    city: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class DoctorOut(BaseModel):
    id: int
    identity_number: str
    first_name: str
    last_name: str
    license_number: str
    specialization: str
    city: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    photo: Optional[bytes] = None
    appointments: List[AppointmentOut] = Field(default_factory=list)
    days: List[DayOut] = Field(default_factory=list)
    services: List[DoctorServiceOut] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)


class UserOut(UserBase):
    id: int
    profile: str
    doctor: Optional[DoctorOut] = None
    appointments: List[AppointmentOut] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
