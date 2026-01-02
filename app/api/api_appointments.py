from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_db
from ..services.service_appointments import (
    create_appointment as create_appointment_service,
    list_appointments as list_appointments_service,
    update_appointment_status,
)

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.post("/", response_model=schemas.AppointmentOut)
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    return create_appointment_service(appointment, db)

@router.get("/", response_model=List[schemas.AppointmentOut])
def list_appointments(
    doctor_id: Optional[int] = None,
    user_id: Optional[str] = None,
    start_from: Optional[datetime] = None,
    start_to: Optional[datetime] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return list_appointments_service(db, doctor_id=doctor_id, user_id=user_id, start_from=start_from, start_to=start_to, status=status)


@router.patch("/{appointment_id}/status", response_model=schemas.AppointmentOut)
def change_status(appointment_id: int, status: str, db: Session = Depends(get_db)):
    return update_appointment_status(appointment_id, status, db)
