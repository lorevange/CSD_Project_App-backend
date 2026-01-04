from fastapi import HTTPException
from sqlalchemy.orm import Session, selectinload

from app import models


def get_review_by_id(review_id: int, db: Session) -> models.Review:
    review = (
        db.query(models.Review)
        .options(selectinload(models.Review.author))
        .filter(
            models.Review.id == review_id,
            models.Review.deleted_at.is_(None),
        )
        .first()
    )
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


def get_reviews_for_doctor(doctor_id: int, db: Session, skip: int = 0, limit: int = 50) -> list[models.Review]:
    return (
        db.query(models.Review)
        .options(selectinload(models.Review.author))
        .filter(
            models.Review.doctor_id == doctor_id,
            models.Review.deleted_at.is_(None),
        )
        .order_by(models.Review.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
