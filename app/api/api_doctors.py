from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from .. import models, schemas
from ..deps import get_db
from ..services.service_user import create_user
from ..services import service_doctor_profiles
from ..queries.query_doctors import get_doctor_detail, search_doctors, get_doctor_by_license_number
from ..services.email import send_verification_email

router = APIRouter(prefix="/doctors", tags=["doctors"])


@router.post("/", response_model=schemas.UserOut)
def create_doctor(doctor: schemas.DoctorCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    if get_doctor_by_license_number(doctor.license_number, db):
        raise HTTPException(status_code=400, detail="There is already a doctor with this license number.")
    
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
    background_tasks.add_task(send_verification_email, db_user.email, db_user.verification_code)
    return db_user


@router.get("/search", response_model=List[schemas.DoctorOut])
def search_doctor(query: str | None = None, city: str | None = None, db: Session = Depends(get_db)):
    return search_doctors(query=query, city=city, db=db)


@router.get("/{doctor_id}", response_model=schemas.DoctorDetailOut)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    return get_doctor_detail(doctor_id, db)


@router.post(
    "/profile",
    response_model=schemas.DoctorProfileResponse,
    response_model_exclude_none=True,
    response_model_by_alias=True,
)
def get_doctor_profile(payload: schemas.DoctorProfileRequest, db: Session = Depends(get_db)):
    return service_doctor_profiles.get_doctor_profile(payload, db)
