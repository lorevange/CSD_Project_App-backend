"""
seed_doctors.py
Creates 10 detailed doctors for MedCare, each with 2-3 services.

Usage:
  1) Ensure .env contains database_url (and DB is reachable)
  2) python seed_doctors.py
"""

from __future__ import annotations

import random
from datetime import datetime, timedelta
from decimal import Decimal

from app.database import SessionLocal, engine, Base
from app import models


def _random_cf() -> str:
    # Simple deterministic-ish fake "codice fiscale" style: 16 alphanumerics
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(random.choice(alphabet) for _ in range(16))


def seed_doctors(n: int = 10) -> None:
    random.seed(42)

    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    first_names = [
        "Marco", "Giulia", "Luca", "Sara", "Francesco",
        "Elena", "Paolo", "Chiara", "Davide", "Anna",
    ]
    last_names = [
        "Rossi", "Bianchi", "Verdi", "Neri", "Gialli",
        "Conti", "Esposito", "Romano", "Ricci", "Marino",
    ]
    specializations = [
        "Cardiologist", "Dermatologist", "Dentist", "Gynecologist", "Orthopedist",
        "Ophthalmologist", "Psychologist", "Nutritionist", "Urologist", "Pediatrician",
    ]

    # Some Italian cities + coordinates (approx)
    locations = [
        ("Rome", "Via del Corso 10", 41.9028, 12.4964),
        ("Milan", "Corso Buenos Aires 25", 45.4642, 9.1900),
        ("Naples", "Via Toledo 120", 40.8518, 14.2681),
        ("Turin", "Via Po 18", 45.0703, 7.6869),
        ("Bologna", "Via Indipendenza 45", 44.4949, 11.3426),
        ("Florence", "Via Calzaiuoli 7", 43.7696, 11.2558),
        ("Genoa", "Via XX Settembre 50", 44.4056, 8.9463),
        ("Venice", "Strada Nova 200", 45.4408, 12.3155),
        ("Verona", "Corso Porta Nuova 9", 45.4384, 10.9916),
        ("Bari", "Corso Vittorio Emanuele II 30", 41.1171, 16.8719),
    ]

    service_catalog = {
        "Cardiologist": [("Cardiology visit", 120), ("ECG", 60), ("Echocardiogram", 140)],
        "Dermatologist": [("Dermatology visit", 100), ("Mole mapping", 90), ("Acne treatment", 80)],
        "Dentist": [("Dental cleaning", 70), ("Tooth whitening", 150), ("Check-up", 50)],
        "Gynecologist": [("Gynecology visit", 130), ("Ultrasound", 90), ("Pap test", 60)],
        "Orthopedist": [("Orthopedic visit", 150), ("Infiltration", 110), ("Post-injury check", 80)],
        "Ophthalmologist": [("Eye visit", 110), ("OCT scan", 95), ("Vision test", 50)],
        "Psychologist": [("Therapy session", 80), ("Initial assessment", 70), ("Follow-up session", 75)],
        "Nutritionist": [("Nutrition plan", 90), ("Body composition", 60), ("Follow-up check", 50)],
        "Urologist": [("Urology visit", 120), ("Ultrasound", 90), ("Follow-up check", 70)],
        "Pediatrician": [("Pediatric visit", 90), ("Growth check", 60), ("Vaccination consult", 50)],
    }

    bios = [
        "Specialist with over 10 years of experience. Focused on evidence-based care and patient education.",
        "Clinical practice centered on precision diagnostics and clear communication with patients and families.",
        "Committed to high-quality care, continuous training, and a patient-first approach.",
        "Experienced professional with a multidisciplinary background and attention to preventive medicine.",
        "Patient-oriented specialist offering clear treatment plans and practical follow-up guidance.",
    ]

    db = SessionLocal()
    created = 0
    skipped = 0

    try:
        for i in range(n):
            fn = first_names[i % len(first_names)]
            ln = last_names[i % len(last_names)]
            spec = specializations[i % len(specializations)]
            city, address, lat, lon = locations[i % len(locations)]

            email = f"{fn.lower()}.{ln.lower()}{i+1}@medcare-demo.test"
            identity_number = _random_cf()
            license_number = f"LIC-{2026}-{1000+i}"

            # Idempotent-ish: skip if email already exists
            existing_user = db.query(models.User).filter(models.User.email == email).first()
            if existing_user:
                skipped += 1
                continue

            # Create User (doctor profile)
            user = models.User(
                first_name=fn,
                last_name=ln,
                identity_number=identity_number,
                profile="doctor",
                email=email,
                phone_number=f"+39{random.randint(3200000000, 3999999999)}",
                password="DemoPass123!",  # NOTE: backend currently compares plaintext
                photo=None,
                is_verified=True,  # make it usable immediately
                verification_code=None,
                verification_expires_at=None,
                last_verification_sent_at=datetime.utcnow() - timedelta(days=1),
            )
            db.add(user)
            db.flush()  # get user.id without committing

            # Create Doctor row (linked 1:1 via user_id)
            doctor = models.Doctor(
                user_id=user.id,
                first_name=fn,
                last_name=ln,
                license_number=license_number,
                specialization=spec,
                city=city,
                address=address,
                latitude=lat,
                longitude=lon,
                information=random.choice(bios),
            )
            db.add(doctor)
            db.flush()  # get doctor.id

            # Create 2–3 services for this doctor
            options = service_catalog.get(spec, [("General consultation", 80), ("Follow-up", 60), ("Report review", 40)])
            random.shuffle(options)
            num_services = random.randint(2, 3)
            for (name, price) in options[:num_services]:
                svc = models.DoctorService(
                    doctor_id=doctor.id,
                    name=name,
                    price=Decimal(str(price)),
                    is_active=True,
                )
                db.add(svc)

            created += 1

        db.commit()
        print(f"✅ Seed completed. Created: {created}, Skipped (already existed): {skipped}")

    except Exception as exc:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_doctors(10)
