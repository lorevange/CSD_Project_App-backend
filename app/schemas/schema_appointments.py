from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.schemas.schema_doctor_services import DoctorServiceOut


class AppointmentDoctorOut(BaseModel):
    id: int
    first_name: str
    last_name: str

    model_config = ConfigDict(from_attributes=True)


class AppointmentUserOut(BaseModel):
    id: int
    first_name: str
    last_name: str

    model_config = ConfigDict(from_attributes=True)


class AppointmentCreate(BaseModel):
    doctor_id: int
    user_id: int
    start_datetime: datetime
    doctor_service_id: int
    examination_type: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[str] = "scheduled"


class AppointmentOut(BaseModel):
    id: int
    doctor_id: int
    user_id: int
    doctor_service_id: int
    start_datetime: datetime
    end_datetime: datetime
    examination_type: str
    price_at_booking: Decimal
    notes: Optional[str] = None
    status: str
    doctor_service: Optional[DoctorServiceOut] = None
    doctor: Optional[AppointmentDoctorOut] = None
    user: Optional[AppointmentUserOut] = None

    model_config = ConfigDict(from_attributes=True)
