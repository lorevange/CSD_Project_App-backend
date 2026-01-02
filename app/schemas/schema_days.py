from datetime import time

from pydantic import BaseModel, ConfigDict


class DayCreate(BaseModel):
    week_day: int
    opening: time
    closing: time
    is_closed: bool
    doctor_id: int


class DayOut(BaseModel):
    id: int
    week_day: int
    opening: time
    closing: time
    is_closed: bool
    doctor_id: int

    model_config = ConfigDict(from_attributes=True)
