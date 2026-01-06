from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_db
from ..services.service_user import create_user
from ..services.email import send_verification_email

router = APIRouter(prefix="/patients", tags=["patients"])


@router.post("/", response_model=schemas.UserOut)
def create_patient(patient: schemas.UserCreateBase, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    db_user = create_user(patient, profile="patient", db=db)
    background_tasks.add_task(send_verification_email, db_user.email, db_user.verification_code)
    return db_user
