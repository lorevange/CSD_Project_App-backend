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



# CREATE CLINIC
# ===========================
@app.post("/clinics", response_model=schemas.ClinicOut)
def create_clinic(clinic: schemas.ClinicCreate, db: Session = Depends(get_db)):
    db_clinic = models.Clinic(
        name=clinic.name,
        address=clinic.address,
        city=clinic.city,
        cap=clinic.cap,
        phone=clinic.phone,
        email=clinic.email
    )
    db.add(db_clinic)
    db.commit()
    db.refresh(db_clinic)
    return db_clinic

# ===========================
# ADD DOCTOR TO CLINIC
# ===========================
@app.post("/clinics/{clinic_id}/add_doctor/{doctor_id}", response_model=schemas.ClinicOut)
def add_doctor_to_clinic(clinic_id: int, doctor_id: str, db: Session = Depends(get_db)):
    clinic = db.query(models.Clinic).filter(models.Clinic.id == clinic_id).first()
    doctor = db.query(models.Doctor).filter(models.Doctor.identity_number == doctor_id).first()
    if not clinic or not doctor:
        raise HTTPException(status_code=404, detail="Clinic or Doctor not found")

    if doctor not in clinic.doctors:
        clinic.doctors.append(doctor)
        db.commit()
        db.refresh(clinic)
    return clinic

# ===========================
# ADD SECRETARY TO CLINIC
# ===========================
@app.post("/clinics/{clinic_id}/add_secretary/{secretary_id}", response_model=schemas.ClinicOut)
def add_secretary_to_clinic(clinic_id: int, secretary_id: str, db: Session = Depends(get_db)):
    clinic = db.query(models.Clinic).filter(models.Clinic.id == clinic_id).first()
    secretary = db.query(models.Secretary).filter(models.Secretary.identity_number == secretary_id).first()
    if not clinic or not secretary:
        raise HTTPException(status_code=404, detail="Clinic or Secretary not found")

    if secretary not in clinic.secretaries:
        clinic.secretaries.append(secretary)
        db.commit()
        db.refresh(clinic)
    return clinic


# CREATE APPOINTMENT
# ===========================
@app.post("/appointments", response_model=schemas.AppointmentOut)
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    # Controllo se doctor, patient e clinic esistono
    doctor = db.query(models.Doctor).filter(models.Doctor.identity_number == appointment.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    patient = db.query(models.Patient).filter(models.Patient.identity_number == appointment.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    clinic = db.query(models.Clinic).filter(models.Clinic.id == appointment.clinic_id).first()
    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")
    
    db_appointment = models.Appointment(
        doctor_id=appointment.doctor_id,
        patient_id=appointment.patient_id,
        clinic_id=appointment.clinic_id,
        datetime=appointment.datetime,
        examination_type=appointment.examination_type,
        notes=appointment.notes,
        status=appointment.status
    )
    
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    
    return db_appointment
