from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from .users import DoctorOut, SecretaryOut


class ClinicBase(BaseModel):
    name: str
    address: str
    city: str
    cap: str
    phone: str
    email: str


class ClinicCreate(ClinicBase):
    pass


class ClinicOut(ClinicBase):
    id: int
    doctors: Optional[List[DoctorOut]] = []
    secretaries: Optional[List[SecretaryOut]] = []

    model_config = ConfigDict(from_attributes=True)
