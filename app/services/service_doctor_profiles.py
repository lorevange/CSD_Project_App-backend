from __future__ import annotations

from decimal import Decimal
from typing import Iterable

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session, selectinload

from app import models, schemas
from app.services import service_appointments, service_reviews


ALLOWED_INCLUDES = {"appointments", "reviews", "reviewsummary"}


def get_doctor_profile(payload: schemas.DoctorProfileRequest, db: Session) -> schemas.DoctorProfileResponse:
    include = _normalize_includes(payload.include)

    doctor = _get_doctor_for_profile(payload.doctor_id, db)
    avg_rating, reviews_count = _get_doctor_stats(doctor.id, db)

    doctor_out = schemas.DoctorProfileOut(
        id=doctor.id,
        name=f"Dr. {doctor.first_name} {doctor.last_name}",
        first_name=doctor.first_name,
        last_name=doctor.last_name,
        specialization=_translated_text(doctor.specialization),
        bio=_translated_text(doctor.information),
        information=doctor.information,
        services=doctor.services,
        price=_lowest_active_price(doctor.services),
        address=doctor.address,
        city=doctor.city,
        latitude=doctor.latitude,
        longitude=doctor.longitude,
        photo=doctor.photo,
        photo_url=None,
        average_rating=float(avg_rating or 0.0),
        reviews_count=int(reviews_count or 0),
    )

    response = schemas.DoctorProfileResponse(doctor=doctor_out)

    if "appointments" in include:
        filters = payload.appointments or schemas.DoctorProfileAppointmentsFilter()
        response.appointments = service_appointments.list_appointments(
            db,
            doctor_id=doctor.id,
            start_from=filters.start_from,
            start_to=filters.start_to,
            status=filters.status,
        )

    if "reviews" in include:
        filters = payload.reviews or schemas.DoctorProfileReviewsFilter()
        response.reviews = _list_reviews_for_doctor(doctor.id, db, filters)

    if "reviewsummary" in include:
        language = payload.review_summary.language if payload.review_summary else None
        response.review_summary = service_reviews.summarize_reviews_for_doctor(doctor.id, db, language)

    return response


def _normalize_includes(values: Iterable[str]) -> set[str]:
    include = set()
    for value in values or []:
        if not value:
            continue
        normalized = value.replace("_", "").strip().lower()
        include.add(normalized)
    unknown = include - ALLOWED_INCLUDES
    if unknown:
        raise HTTPException(status_code=400, detail=f"Unknown include values: {sorted(unknown)}")
    return include


def _get_doctor_for_profile(doctor_id: int, db: Session) -> models.Doctor:
    doctor = (
        db.query(models.Doctor)
        .options(
            selectinload(models.Doctor.services),
            selectinload(models.Doctor.user),
        )
        .filter(models.Doctor.id == doctor_id)
        .first()
    )
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


def _get_doctor_stats(doctor_id: int, db: Session) -> tuple[float, int]:
    stats = (
        db.query(
            func.coalesce(func.avg(models.Review.rating), 0),
            func.count(models.Review.id),
        )
        .filter(
            models.Review.doctor_id == doctor_id,
            models.Review.deleted_at.is_(None),
        )
        .first()
    )
    avg_rating, reviews_count = stats
    return float(avg_rating or 0.0), int(reviews_count or 0)


def _list_reviews_for_doctor(
    doctor_id: int,
    db: Session,
    filters: schemas.DoctorProfileReviewsFilter,
) -> list[models.Review]:
    sort = (filters.sort or "created_at_desc").strip().lower()
    if sort not in {"created_at_desc", "created_at_asc"}:
        raise HTTPException(status_code=400, detail="reviews.sort must be created_at_desc or created_at_asc")

    query = (
        db.query(models.Review)
        .options(selectinload(models.Review.author))
        .filter(
            models.Review.doctor_id == doctor_id,
            models.Review.deleted_at.is_(None),
        )
    )
    if sort == "created_at_asc":
        query = query.order_by(models.Review.created_at.asc())
    else:
        query = query.order_by(models.Review.created_at.desc())

    limit = max(1, min(filters.limit, 200))
    return query.limit(limit).all()


def _lowest_active_price(services: Iterable[models.DoctorService]) -> Decimal | None:
    active_prices = [service.price for service in services if service.is_active]
    if not active_prices:
        return None
    return min(active_prices)


def _translated_text(value: str | None) -> schemas.TranslatedText:
    return schemas.TranslatedText(it=value, en=value)
