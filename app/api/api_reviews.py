from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import schemas, models
from app.auth import get_current_user
from app.deps import get_db
from app.services import service_reviews

router = APIRouter(tags=["reviews"])


@router.post("/doctors/{doctor_id}/reviews", response_model=schemas.ReviewOut, status_code=status.HTTP_201_CREATED)
def create_review_for_doctor(
    doctor_id: int,
    body: schemas.ReviewCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return service_reviews.create_review(doctor_id, body, current_user, db)


@router.get("/doctors/{doctor_id}/reviews", response_model=List[schemas.ReviewOut])
def list_reviews_for_doctor(
    doctor_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    return service_reviews.list_reviews_for_doctor(doctor_id, db, skip=skip, limit=limit)


@router.patch("/reviews/{review_id}", response_model=schemas.ReviewOut)
def update_review(
    review_id: int,
    body: schemas.ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return service_reviews.update_review(review_id, body, current_user, db)


@router.delete("/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    service_reviews.delete_review(review_id, current_user, db)
    return None
