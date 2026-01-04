from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas
from app.deps import get_db
from app.services import service_doctor_services

router = APIRouter(prefix="/doctor-services", tags=["doctor-services"])


@router.post("/", response_model=schemas.DoctorServiceOut)
def create_doctor_service(body: schemas.DoctorServiceCreate, db: Session = Depends(get_db)):
    return service_doctor_services.create_service(body, db)


@router.get("/", response_model=List[schemas.DoctorServiceOut])
def list_doctor_services(
    doctor_id: Optional[int] = None,
    include_inactive: bool = False,
    db: Session = Depends(get_db),
):
    return service_doctor_services.list_services(db, doctor_id=doctor_id, include_inactive=include_inactive)


@router.get("/{service_id}", response_model=schemas.DoctorServiceOut)
def get_doctor_service(service_id: int, db: Session = Depends(get_db)):
    return service_doctor_services.get_service(service_id, db)


@router.patch("/{service_id}", response_model=schemas.DoctorServiceOut)
def update_doctor_service(service_id: int, body: schemas.DoctorServiceUpdate, db: Session = Depends(get_db)):
    return service_doctor_services.update_service(service_id, body, db)


@router.delete("/{service_id}", status_code=204)
def delete_doctor_service(service_id: int, db: Session = Depends(get_db)):
    service_doctor_services.delete_service(service_id, db)
    return None
