from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import models
from ..auth import verify_password


def get_user_by_email_and_password(email: str, password: str, db: Session) -> models.User:
    user = (
        db.query(models.User)
        .filter(models.User.email == email)
        .first()
    )
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    if user.password != password:
        raise HTTPException(status_code=404, detail="Wrong Password.")
    return user