from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, DataError

from . import models, schemas
from .database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ===========================
# CREATE PATIENT
# ===========================
@app.post("/patients", response_model=schemas.UserOut)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    db_user = models.User(
        first_name=patient.first_name,
        last_name=patient.last_name,
        identity_number=patient.identity_number,
        profile="patient",
        email=patient.email,
        phone_number=patient.phone_number,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    db_patient = models.Patient(
        identity_number=patient.identity_number,
        prova=patient.prova,
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_user)

    return db_user


# ===========================
# CREATE DOCTOR
# ===========================
@app.post("/doctors", response_model=schemas.UserOut)
def create_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    db_user = models.User(
        first_name=doctor.first_name,
        last_name=doctor.last_name,
        identity_number=doctor.identity_number,
        profile="doctor",
        email=doctor.email,
        phone_number=doctor.phone_number,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    db_doctor = models.Doctor(
        identity_number=doctor.identity_number,
        license_number=doctor.license_number,
        specialization=doctor.specialization,
    )
    db.add(db_doctor)
    db.commit()
    db.refresh(db_user)

    return db_user


# ===========================
# CREATE ADMIN
# ===========================
@app.post("/admins", response_model=schemas.UserOut)
def create_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    db_user = models.User(
        first_name=admin.first_name,
        last_name=admin.last_name,
        identity_number=admin.identity_number,
        profile="admin",
        email=admin.email,
        phone_number=admin.phone_number,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    db_admin = models.Admin(
        identity_number=admin.identity_number,
        is_superadmin=admin.is_superadmin,
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_user)

    return db_user


# ===========================
# CREATE SECRETARY
# ===========================
@app.post("/secretaries", response_model=schemas.UserOut)
def create_secretary(secretary: schemas.SecretaryCreate, db: Session = Depends(get_db)):
    db_user = models.User(
        first_name=secretary.first_name,
        last_name=secretary.last_name,
        identity_number=secretary.identity_number,
        profile="secretary",
        email=secretary.email,
        phone_number=secretary.phone_number,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    db_secretary = models.Secretary(
        identity_number=secretary.identity_number,
        prova=secretary.prova,
    )
    db.add(db_secretary)
    db.commit()
    db.refresh(db_user)

    return db_user


# ===========================
# LIST USERS
# ===========================
@app.get("/users", response_model=list[schemas.UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()
