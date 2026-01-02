from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models
from app.queries.query_doctors import get_doctor_by_id
from app.queries.query_users import get_user_by_identity_number
from app.queries.query_appointments import get_appointment_by_id


def _normalize_slot(start: datetime) -> datetime:
    """Ensure start time aligns to 30-minute slots."""
    if start.minute not in (0, 30) or start.second != 0 or start.microsecond != 0:
        raise HTTPException(status_code=400, detail="start_datetime must align to 30-minute slots (HH:00 or HH:30)")
    return start


def create_appointment(payload, db: Session) -> models.Appointment:
    # Validate foreign keys
    doctor = get_doctor_by_id(payload.doctor_id, db)
    user = get_user_by_identity_number(payload.user_id, db)

    start = _normalize_slot(payload.start_datetime)
    end = start + models.Appointment.default_duration()
    status = payload.status or "scheduled"

    # Check conflicts on the same slot for the doctor
    conflict = (
        db.query(models.Appointment)
        .filter(
            models.Appointment.doctor_id == doctor.id,
            models.Appointment.start_datetime == start,
            models.Appointment.status == "scheduled",
        )
        .first()
    )
    if conflict:
        raise HTTPException(status_code=409, detail="Slot not available")

    appt = models.Appointment(
        doctor_id=doctor.id,
        user_id=user.identity_number,
        start_datetime=start,
        end_datetime=end,
        examination_type=payload.examination_type,
        notes=payload.notes,
        status=status,
    )
    db.add(appt)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # Unique constraint fallback
        raise HTTPException(status_code=409, detail="Slot not available")
    db.refresh(appt)
    return appt


def list_appointments(db: Session, doctor_id: int | None = None, user_id: str | None = None,
                      start_from: datetime | None = None, start_to: datetime | None = None) -> list[models.Appointment]:
    query = db.query(models.Appointment)
    if doctor_id:
        query = query.filter(models.Appointment.doctor_id == doctor_id)
    if user_id:
        query = query.filter(models.Appointment.user_id == user_id)
    if start_from:
        query = query.filter(models.Appointment.start_datetime >= start_from)
    if start_to:
        query = query.filter(models.Appointment.start_datetime <= start_to)
    return query.order_by(models.Appointment.start_datetime.asc()).all()


def update_appointment_status(appointment_id: int, status: str, db: Session) -> models.Appointment:
    appt = get_appointment_by_id(appointment_id, db)
    appt.status = status
    db.commit()
    db.refresh(appt)
    return appt
