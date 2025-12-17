from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.models import User

from app.deps import get_db
from app.auth import create_access_token
from app.queries.query_users import authenticate_user
from app.schemas import LoginRequest, LoginResponse
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import create_access_token, get_current_user
from app.deps import get_db
from app.queries.query_users import authenticate_user
from app.schemas import LoginRequest, LoginResponse, UserOut
from app.models import User
router = APIRouter(prefix="/users", tags=["users"])


@router.post("/login/", response_model=LoginResponse)  # aggiunto slash finale
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """
    Login di un utente con email e password.
    Restituisce token JWT + dati utente.
    """
    user = authenticate_user(data.email, data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.email})

    # Restituiamo solo campi serializzabili con UserOut
    user_data = UserOut.from_orm(user)

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=user_data
    )



@router.get("/me", response_model=UserOut)
def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Restituisce i dati dell'utente loggato (endpoint protetto)
    """
    return UserOut.from_orm(current_user)
