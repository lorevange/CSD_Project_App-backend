from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import models


def get_patient_by_id(patient_id: str, db: Session) -> models.Patient:
    patient = db.query(models.Patient).filter(models.Patient.identity_number == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient
