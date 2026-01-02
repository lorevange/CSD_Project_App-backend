from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import models
from app.queries.query_doctors import get_doctor_by_id


def _get_service_or_404(service_id: int, db: Session) -> models.DoctorService:
    service = db.query(models.DoctorService).filter(models.DoctorService.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


def create_service(payload, db: Session) -> models.DoctorService:
    get_doctor_by_id(payload.doctor_id, db)
    service = models.DoctorService(
        doctor_id=payload.doctor_id,
        name=payload.name,
        price=payload.price,
        is_active=payload.is_active,
    )
    db.add(service)
    db.commit()
    db.refresh(service)
    return service


def list_services(db: Session, doctor_id: int | None = None, include_inactive: bool = False) -> list[models.DoctorService]:
    query = db.query(models.DoctorService)
    if doctor_id:
        query = query.filter(models.DoctorService.doctor_id == doctor_id)
    if not include_inactive:
        query = query.filter(models.DoctorService.is_active.is_(True))
    return query.order_by(models.DoctorService.name.asc()).all()


def get_service(service_id: int, db: Session) -> models.DoctorService:
    return _get_service_or_404(service_id, db)


def update_service(service_id: int, payload, db: Session) -> models.DoctorService:
    service = _get_service_or_404(service_id, db)

    if payload.name is not None:
        service.name = payload.name
    if payload.price is not None:
        service.price = payload.price
    if payload.is_active is not None:
        service.is_active = payload.is_active

    db.commit()
    db.refresh(service)
    return service


def delete_service(service_id: int, db: Session) -> None:
    service = _get_service_or_404(service_id, db)
    db.delete(service)
    db.commit()
