from datetime import datetime

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from app.auth import create_access_token, get_current_user
from app.deps import get_db
from app.queries.query_users import get_user_by_email, get_user_by_email_and_password
from app.schemas import (
    LoginRequest,
    LoginResponse,
    UserOut,
    UserEdit,
    VerifyEmailRequest,
    ResendVerificationRequest,
)
router = APIRouter(prefix="/users", tags=["users"])
from ..services.service_user import edit_user, refresh_verification_code
from ..services.email import send_verification_email

@router.post("/login/", response_model=LoginResponse)  # aggiunto slash finale
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """
    Login di un utente con email e password.
    Restituisce token JWT + dati utente.
    """
    user = get_user_by_email_and_password(data.email, data.password, db)

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified.",
        )

    access_token = create_access_token({"sub": user.email})

    # Restituiamo solo campi serializzabili con UserOut
    user_data = UserOut.from_orm(user)

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=user_data
    )


@router.get("/me", response_model=UserOut)
def validate_token(
    authorization: str | None = Header(default=None, alias="Authorization"),
    db: Session = Depends(get_db),
):
    """
    Endpoint protetto per validare il token JWT.
    Restituisce i dati dell'utente autenticato.
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    current_user = get_current_user(token=token, db=db)
    return UserOut.from_orm(current_user)


@router.post("/update/", response_model=UserOut)
def update_user(body: UserEdit, db: Session = Depends(get_db)):
    return edit_user(body.identity_number, body.first_name, body.last_name, body.photo, body.information, db)


@router.post("/verify-email")
def verify_email(body: VerifyEmailRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(body.email, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    if user.is_verified:
        return {"status": "already_verified"}

    if (
        not user.verification_code
        or user.verification_code != body.code
        or not user.verification_expires_at
        or user.verification_expires_at < datetime.utcnow()
    ):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired code.")

    user.is_verified = True
    user.verification_code = None
    user.verification_expires_at = None
    db.commit()

    return {"status": "verified"}


@router.post("/resend-verification")
def resend_verification(
    body: ResendVerificationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    user = get_user_by_email(body.email, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    if user.is_verified:
        return {"status": "already_verified"}

    code = refresh_verification_code(user, db)
    background_tasks.add_task(send_verification_email, user.email, code)

    return {"status": "sent"}
