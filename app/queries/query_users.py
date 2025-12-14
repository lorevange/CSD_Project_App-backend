from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import models


def get_user_by_email_and_password(email: str, password: str, db: Session) -> models.User:
    user = (
        db.query(models.User)
        .filter(models.User.email == email, models.User.password == password)
        .first()
    )
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_user_by_email(email: str, db: Session) -> models.User:
    user = (
        db.query(models.User)
        .filter(models.User.email == email)
        .first()
    )
    return user