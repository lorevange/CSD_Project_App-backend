from sqlalchemy.orm import Session
from fastapi import HTTPException
from app import models, schemas
from app.auth import get_password_hash
from ..queries.query_users import get_user_by_email, get_user_by_identity_number

def create_user(base: schemas.UserCreateBase, profile: str, db: Session) -> models.User:
    if get_user_by_email(base.email, db):
        raise HTTPException(status_code=409, detail="Email already registered")

    user = models.User(
        first_name=base.first_name,
        last_name=base.last_name,
        identity_number=base.identity_number,
        profile=profile,
        email=base.email,
        phone_number=base.phone_number,
        password=get_password_hash(base.password),  # 🔐 HASH QUI
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def edit_user(identity_number: str, first_name: str, last_name: str, db: Session) -> models.User:
    user = get_user_by_identity_number(identity_number, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.first_name = first_name
    user.last_name = last_name

    db.commit()
    db.refresh(user)
    return user
