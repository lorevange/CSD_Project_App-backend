from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserCreateBase(BaseModel):
    first_name: str
    last_name: str
    identity_number: str
    email: str
    phone_number: Optional[str] = None
    password: str


class UserBase(BaseModel):
    first_name: str
    last_name: str
    identity_number: str
    email: str
    phone_number: Optional[str] = None


class DoctorCreate(UserCreateBase):
    license_number: str
    specialization: str


class DoctorOut(BaseModel):
    identity_number: str
    first_name: str
    last_name: str
    license_number: str
    specialization: str
    model_config = ConfigDict(from_attributes=True)


class UserOut(UserBase):
    id: str
    profile: str
    doctor: Optional[DoctorOut] = None

    model_config = ConfigDict(from_attributes=True)
