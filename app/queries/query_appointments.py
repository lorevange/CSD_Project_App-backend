from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import models


def get_appointment_by_id(appointment_id: int, db: Session) -> models.Appointment:
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment
