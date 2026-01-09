import secrets
from datetime import datetime, timedelta

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

    verification_code = f"{secrets.randbelow(90000) + 10000:05}"
    verification_expires_at = datetime.utcnow() + timedelta(minutes=10)
    now = datetime.utcnow()

    user = models.User(
        first_name=base.first_name,
        last_name=base.last_name,
        identity_number=base.identity_number,
        profile=profile,
        email=base.email,
        phone_number=base.phone_number,
        password=base.password,
        photo=base.photo,
        verification_code=verification_code,
        verification_expires_at=verification_expires_at,
        last_verification_sent_at=now,
        is_verified=False,
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


def refresh_verification_code(user: models.User, db: Session, cooldown_seconds: int = 60) -> str:
    """Regenerate verification code with a cooldown to prevent spamming."""
    now = datetime.utcnow()
    if user.last_verification_sent_at and (now - user.last_verification_sent_at).total_seconds() < cooldown_seconds:
        raise HTTPException(status_code=429, detail="Please wait before requesting a new code.")

    user.verification_code = f"{secrets.randbelow(90000) + 10000:05}"
    user.verification_expires_at = now + timedelta(minutes=10)
    user.last_verification_sent_at = now
    db.commit()
    db.refresh(user)
    return user.verification_code
