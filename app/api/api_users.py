from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_db
from ..queries.query_users import get_user_by_email_and_password
from ..services.service_user import edit_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[schemas.UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@router.post("/login/", response_model=schemas.UserOut)
def get_user_by_email_and_pw(body: schemas.LoginRequest, db: Session = Depends(get_db)):
    return get_user_by_email_and_password(body.email, body.password, db)

@router.post("/update/", response_model=schemas.UserOut)
def update_user(body: schemas.UserEdit, db: Session = Depends(get_db)):
    return edit_user(body.identity_number, body.first_name, body.last_name, db)
