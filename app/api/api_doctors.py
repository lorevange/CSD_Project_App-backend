from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_db
from ..services.service_user import create_user
from ..queries.query_doctors import get_doctor_by_id, search_doctors

router = APIRouter(prefix="/doctors", tags=["doctors"])


@router.post("/", response_model=schemas.UserOut)
def create_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    db_user = create_user(doctor, profile="doctor", db=db)
    db_doctor = models.Doctor(
        user_id=db_user.id,
        first_name=doctor.first_name,
        last_name=doctor.last_name,
        license_number=doctor.license_number,
        specialization=doctor.specialization,
        city=doctor.city,
        address=doctor.address,
        latitude=doctor.latitude,
        longitude=doctor.longitude,
        information=doctor.information,
    )
    db.add(db_doctor)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/search", response_model=List[schemas.DoctorOut])
def search_doctor(query: str | None = None, city: str | None = None, db: Session = Depends(get_db)):
    return search_doctors(query=query, city=city, db=db)


@router.get("/{doctor_id}", response_model=schemas.DoctorOut)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    return get_doctor_by_id(doctor_id, db)
