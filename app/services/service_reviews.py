from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import models
from app.queries.query_doctors import get_doctor_by_id
from app.queries.query_reviews import get_review_by_id, get_reviews_for_doctor


def create_review(doctor_id: int, payload, current_user: models.User, db: Session) -> models.Review:
    doctor = get_doctor_by_id(doctor_id, db)

    if current_user.profile == "doctor" and current_user.doctor and current_user.doctor.id == doctor.id:
        raise HTTPException(status_code=400, detail="Doctors cannot review themselves")

    existing = (
        db.query(models.Review)
        .filter(
            models.Review.doctor_id == doctor.id,
            models.Review.author_id == current_user.id,
        )
        .first()
    )
    if existing:
        if existing.deleted_at is not None:
            existing.rating = payload.rating
            existing.comment = payload.comment
            existing.deleted_at = None
            existing.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(existing)
            return existing
        raise HTTPException(status_code=400, detail="You have already reviewed this doctor")

    review = models.Review(
        doctor_id=doctor.id,
        author_id=current_user.id,
        rating=payload.rating,
        comment=payload.comment,
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


def list_reviews_for_doctor(doctor_id: int, db: Session, skip: int = 0, limit: int = 50) -> list[models.Review]:
    get_doctor_by_id(doctor_id, db)
    return get_reviews_for_doctor(doctor_id, db, skip=skip, limit=limit)


def update_review(review_id: int, payload, current_user: models.User, db: Session) -> models.Review:
    review = get_review_by_id(review_id, db)
    if review.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only edit your own reviews")

    if payload.rating is not None:
        review.rating = payload.rating
    if payload.comment is not None:
        review.comment = payload.comment
    review.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(review)
    return review


def delete_review(review_id: int, current_user: models.User, db: Session) -> None:
    review = get_review_by_id(review_id, db)
    if review.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own reviews")
    review.deleted_at = datetime.utcnow()
    review.updated_at = datetime.utcnow()
    db.commit()
