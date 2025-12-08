from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_db
from ..queries.query_users import get_user_by_email_and_password

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[schemas.UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@router.post("/login/", response_model=schemas.UserOut)
def get_user_by_email_and_pw(body: schemas.LoginRequest, db: Session = Depends(get_db)):
    return get_user_by_email_and_password(body.email, body.password, db)
