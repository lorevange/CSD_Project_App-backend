from sqlalchemy.orm import Session
from fastapi import HTTPException

from app import models, schemas
from ..queries.query_users import get_user_by_email


def create_user(base: schemas.UserCreateBase, profile: str, db: Session) -> models.User:
    """Create and persist a base User row."""
    if get_user_by_email(base.email, db):
        raise HTTPException(status_code=404, detail="There is already a user associated to this email.")
    
    user = models.User(
        first_name=base.first_name,
        last_name=base.last_name,
        identity_number=base.identity_number,
        profile=profile,
        email=base.email,
        phone_number=base.phone_number,
        password=base.password,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
