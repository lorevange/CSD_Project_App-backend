from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_db
from ..services.service_user import create_user

router = APIRouter(prefix="/patients", tags=["patients"])


@router.post("/", response_model=schemas.UserOut)
def create_patient(patient: schemas.UserBase, db: Session = Depends(get_db)):
    db_user = create_user(patient, profile="patient", db=db)
    return db_user