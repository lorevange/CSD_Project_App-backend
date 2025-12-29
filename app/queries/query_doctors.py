from fastapi import HTTPException
from sqlalchemy import case, or_
from sqlalchemy.orm import Session

from app import models

def get_doctor_by_id(doctor_id: str, db: Session) -> models.Doctor:
    doctor = db.query(models.Doctor).filter(models.Doctor.identity_number == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


def search_doctors(db: Session, query: str | None = None, city: str | None = None) -> list[models.Doctor]:
    if not query and not city:
        return db.query(models.Doctor).order_by(
            models.Doctor.last_name.asc(),
            models.Doctor.first_name.asc()
        ).all()
    
    like = f"%{query}%"
    city_like = f"%{city}%"
    query_obj
    score = (
        case((models.Doctor.address.ilike(like), 3), else_=0)
        + case((models.Doctor.last_name.ilike(like), 2), else_=0)
        + case((models.Doctor.specialization.ilike(like), 2), else_=0)
        + case((models.Doctor.first_name.ilike(like), 1), else_=0)
    )

    if query:
        query_obj = db.query(models.Doctor).filter(
            or_(
                models.Doctor.first_name.ilike(like),
                models.Doctor.last_name.ilike(like),
                models.Doctor.address.ilike(like),
                models.Doctor.specialization.ilike(like),
            )
        )
        if city:
            query_obj = query_obj.filter(models.Doctor.city.ilike(city_like))

    if city and not query:
        query_obj = db.query(models.Doctor).filter(models.Doctor.city.ilike(city_like))

    return query_obj.order_by(
        score.desc(),
        models.Doctor.last_name.asc(),
        models.Doctor.first_name.asc()
    ).all()
