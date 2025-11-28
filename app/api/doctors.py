from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_db
from ..services.users import create_user
from ..queries.query_doctors import get_doctors_by_clinic_id

router = APIRouter(prefix="/doctors", tags=["doctors"])


@router.post("/", response_model=schemas.UserOut)
def create_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    db_user = create_user(doctor, profile="doctor", db=db)
    db_doctor = models.Doctor(
        identity_number=doctor.identity_number,
        first_name=doctor.first_name,
        last_name=doctor.last_name,
        license_number=doctor.license_number,
        specialization=doctor.specialization,
    )
    db.add(db_doctor)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/{clinic_id}", response_model=list[schemas.DoctorOut])
def list_doctors_by_clinic(clinic_id: int, db: Session = Depends(get_db)):
    return get_doctors_by_clinic_id(clinic_id, db)
