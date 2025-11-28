from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_db
from ..services.users import create_user

router = APIRouter(prefix="/secretaries", tags=["secretaries"])


@router.post("/", response_model=schemas.UserOut)
def create_secretary(secretary: schemas.SecretaryCreate, db: Session = Depends(get_db)):
    db_user = create_user(secretary, profile="secretary", db=db)
    db_secretary = models.Secretary(identity_number=secretary.identity_number, prova=secretary.prova)
    db.add(db_secretary)
    db.commit()
    db.refresh(db_user)
    return db_user
