from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_db
from ..services.users import create_user

router = APIRouter(prefix="/admins", tags=["admins"])


@router.post("/", response_model=schemas.UserOut)
def create_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    db_user = create_user(admin, profile="admin", db=db)
    db_admin = models.Admin(identity_number=admin.identity_number, is_superadmin=admin.is_superadmin)
    db.add(db_admin)
    db.commit()
    db.refresh(db_user)
    return db_user
