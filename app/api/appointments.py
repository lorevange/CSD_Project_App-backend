from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_db
from ..queries.query_clinics import get_clinic_by_id
from ..queries.query_doctors import get_doctor_by_id
from ..queries.query_patients import get_patient_by_id

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.post("/", response_model=schemas.AppointmentOut)
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    doctor = get_doctor_by_id(appointment.doctor_id, db)
    get_patient_by_id(appointment.patient_id, db)
    get_clinic_by_id(appointment.clinic_id, db)

    db_appointment = models.Appointment(
        doctor_id=doctor.identity_number,
        patient_id=appointment.patient_id,
        clinic_id=appointment.clinic_id,
        datetime=appointment.datetime,
        examination_type=appointment.examination_type,
        notes=appointment.notes,
        status=appointment.status,
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment
