from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import models

def get_doctor_by_id(doctor_id: str, db: Session) -> models.Doctor:
    doctor = db.query(models.Doctor).filter(models.Doctor.identity_number == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor