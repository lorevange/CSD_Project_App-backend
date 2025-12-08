from sqlalchemy.orm import Session

from app import models, schemas


def create_user(base: schemas.UserCreateBase, profile: str, db: Session) -> models.User:
    """Create and persist a base User row."""
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
