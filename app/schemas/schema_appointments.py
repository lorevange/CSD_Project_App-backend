from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AppointmentCreate(BaseModel):
    doctor_id: str
    datetime: datetime
    examination_type: str
    notes: Optional[str] = None
    status: Optional[str] = "scheduled"


class AppointmentOut(BaseModel):
    id: int
    doctor_id: str
    datetime: datetime
    examination_type: str
    notes: Optional[str] = None
    status: str

    model_config = ConfigDict(from_attributes=True)
