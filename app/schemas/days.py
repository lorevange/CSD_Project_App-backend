from datetime import time
from pydantic import BaseModel, ConfigDict


class DayCreate(BaseModel):
    week_day: str
    open: time
    close: time
    clinic_id: int


class DayOut(BaseModel):
    id: int
    week_day: str
    open: time
    close: time
    clinic_id: int

    model_config = ConfigDict(from_attributes=True)
