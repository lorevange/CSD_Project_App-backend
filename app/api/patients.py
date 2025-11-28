from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_db
from ..services.users import create_user

router = APIRouter(prefix="/patients", tags=["patients"])


@router.post("/", response_model=schemas.UserOut)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    db_user = create_user(patient, profile="patient", db=db)
    db_patient = models.Patient(identity_number=patient.identity_number, prova=patient.prova)
    db.add(db_patient)
    db.commit()
    db.refresh(db_user)
    return db_user
