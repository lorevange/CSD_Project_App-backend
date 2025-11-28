from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import models


def get_secretary_by_id(secretary_id: str, db: Session) -> models.Secretary:
    secretary = (
        db.query(models.Secretary).filter(models.Secretary.identity_number == secretary_id).first()
    )
    if not secretary:
        raise HTTPException(status_code=404, detail="Secretary not found")
    return secretary
