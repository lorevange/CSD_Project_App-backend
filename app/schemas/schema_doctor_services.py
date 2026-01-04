from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DoctorServiceBase(BaseModel):
    name: str
    price: Decimal
    is_active: bool = True


class DoctorServiceCreate(DoctorServiceBase):
    doctor_id: int


class DoctorServiceUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[Decimal] = None
    is_active: Optional[bool] = None


class DoctorServiceOut(DoctorServiceBase):
    id: int
    doctor_id: int

    model_config = ConfigDict(from_attributes=True)
