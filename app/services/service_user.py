from sqlalchemy.orm import Session
from fastapi import HTTPException

from app import models, schemas
from ..queries.query_users import get_user_by_email, get_user_by_identity_number

def create_user(base: schemas.UserCreateBase, profile: str, db: Session) -> models.User:
    """Create and persist a base User row."""
    if get_user_by_email(base.email, db):
        raise HTTPException(status_code=404, detail="There is already a user associated to this email.")
    if get_user_by_identity_number(base.identity_number, db):
        raise HTTPException(status_code=404, detail="There is already a user associated to this identity_number.")
    user = models.User(
        first_name=base.first_name,
        last_name=base.last_name,
        identity_number=base.identity_number,
        profile=profile,
        email=base.email,
        phone_number=base.phone_number,
        password=base.password,
        photo=base.photo,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def edit_user(identity_number: str, first_name: str, last_name: str, photo: bytes, information: str | None, db: Session) -> models.User:
    user = get_user_by_identity_number(identity_number, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.first_name = first_name
    user.last_name = last_name
    if photo is not None:
        user.photo = photo

    if user.profile == 'doctor':
        doctor = db.query(models.Doctor).filter(models.Doctor.user_id == user.id).first()
        if doctor:
            doctor.first_name = first_name
            doctor.last_name = last_name
            doctor.information = information

    db.commit()
    db.refresh(user)
    return user
