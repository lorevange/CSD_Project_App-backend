# CSD Backend

FastAPI backend for a doctor/patient appointment platform.

## Tech Stack
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic Settings
- JWT authentication (`python-jose`)

## Project Structure
- `app/main.py`: FastAPI app and router registration
- `app/api/`: API endpoints
- `app/models/`: SQLAlchemy models
- `app/schemas/`: Pydantic schemas
- `app/services/`: business logic
- `app/queries/`: database query helpers
- `create_tables.py`: optional DB table initialization script
- `generate_doctors.py`: utility script for doctor data generation

## Requirements
- Python 3.10+
- PostgreSQL running locally or remotely

## Setup
1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root with at least:
   ```env
   DATABASE_URL=postgresql+psycopg://<user>:<password>@<host>:<port>/<db_name>

   # Optional (AI summary features)
   OPENAI_API_KEY=
   OPENAI_MODEL=gpt-3.5-turbo
   GEMINI_API_KEY=
   GEMINI_MODEL=gemini-1.5-flash-001

   # Optional (email verification)
   SMTP_HOST=
   SMTP_PORT=
   SMTP_USERNAME=
   SMTP_PASSWORD=
   SMTP_FROM=
   ```

## Run the API
```bash
uvicorn app.main:app --reload
```

Default local URL:
- API: `http://127.0.0.1:8000`
- Docs (Swagger): `http://127.0.0.1:8000/docs`

## Main Endpoints
- `POST /users/login/`
- `GET /users/me`
- `POST /users/update/`
- `POST /users/verify-email`
- `POST /users/resend-verification`
- `POST /patients/`
- `POST /doctors/`
- `GET /doctors/search`
- `GET /doctors/{doctor_id}`
- `POST /appointments/`
- `GET /appointments/`
- `PATCH /appointments/{appointment_id}/status`
- `POST /doctor-services/`
- `GET /doctor-services/`
- `PATCH /doctor-services/{service_id}`
- `DELETE /doctor-services/{service_id}`
- `POST /doctors/{doctor_id}/reviews`
- `GET /doctors/{doctor_id}/reviews`
- `GET /doctors/{doctor_id}/reviews/summary`

## Notes
- CORS is enabled for `http://localhost:3000` and `http://localhost:5173`.
- Tables are currently created from app startup via SQLAlchemy metadata in `app/main.py`.
