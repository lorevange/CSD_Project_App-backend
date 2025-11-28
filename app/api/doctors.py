from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_db
from ..services.users import create_user

router = APIRouter(prefix="/doctors", tags=["doctors"])


@router.post("/", response_model=schemas.UserOut)
def create_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    db_user = create_user(doctor, profile="doctor", db=db)
    db_doctor = models.Doctor(
        identity_number=doctor.identity_number,
        license_number=doctor.license_number,
        specialization=doctor.specialization,
    )
    db.add(db_doctor)
    db.commit()
    db.refresh(db_user)
    return db_user
