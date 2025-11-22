from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine
from .deps import get_db

models.Base.metadata.create_all(bind=engine)  # OK for uni/dev; use Alembic later

app = FastAPI()


@app.post("/users", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        identity_number=user.identity_number,
        profile=user.profile,
        email=user.email,
        phone_number=user.phone_number,
    )
    db.add(db_user)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="A user with this Identity Number already exists.",
        ) from exc
    except DataError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="A field has more characters than it is allowed.",
        ) from exc
    db.refresh(db_user)
    return db_user


@app.get("/users", response_model=list[schemas.UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()
