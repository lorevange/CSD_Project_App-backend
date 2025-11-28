from fastapi import FastAPI
from .database import engine, Base
from .api import (
    users as users_api,
    patients as patients_api,
    doctors as doctors_api,
    admins as admins_api,
    secretaries as secretaries_api,
    clinics as clinics_api,
    appointments as appointments_api,
)

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users_api.router)
app.include_router(patients_api.router)
app.include_router(doctors_api.router)
app.include_router(admins_api.router)
app.include_router(secretaries_api.router)
app.include_router(clinics_api.router)
app.include_router(appointments_api.router)
