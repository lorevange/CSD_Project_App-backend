from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import models


def get_clinic_by_id(clinic_id: int, db: Session) -> models.Clinic:
    clinic = db.query(models.Clinic).filter(models.Clinic.id == clinic_id).first()
    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")
    return clinic
