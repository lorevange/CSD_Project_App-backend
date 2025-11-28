from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_db
from ..queries.query_clinics import get_clinic_by_id
from ..queries.query_doctors import get_doctor_by_id
from ..queries.query_secretaries import get_secretary_by_id

router = APIRouter(prefix="/clinics", tags=["clinics"])


@router.post("/", response_model=schemas.ClinicOut)
def create_clinic(clinic: schemas.ClinicCreate, db: Session = Depends(get_db)):
    db_clinic = models.Clinic(
        name=clinic.name,
        address=clinic.address,
        city=clinic.city,
        cap=clinic.cap,
        phone=clinic.phone,
        email=clinic.email,
    )
    db.add(db_clinic)
    db.commit()
    db.refresh(db_clinic)
    return db_clinic


@router.post("/{clinic_id}/add_doctor/{doctor_id}", response_model=schemas.ClinicOut)
def add_doctor_to_clinic(clinic_id: int, doctor_id: str, db: Session = Depends(get_db)):
    clinic = get_clinic_by_id(clinic_id, db)
    doctor = get_doctor_by_id(doctor_id, db)

    if doctor not in clinic.doctors:
        clinic.doctors.append(doctor)
        db.commit()
        db.refresh(clinic)
    return clinic


@router.post("/{clinic_id}/add_secretary/{secretary_id}", response_model=schemas.ClinicOut)
def add_secretary_to_clinic(clinic_id: int, secretary_id: str, db: Session = Depends(get_db)):
    clinic = get_clinic_by_id(clinic_id, db)
    secretary = get_secretary_by_id(secretary_id, db)

    if secretary not in clinic.secretaries:
        clinic.secretaries.append(secretary)
        db.commit()
        db.refresh(clinic)
    return clinic
