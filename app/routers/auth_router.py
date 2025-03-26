from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.services.auth import verify_password, create_access_token
from app.models.user_model import User
from app.config.database import get_db

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


# Endpoint login
@router.post("/login")
def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    # Buscar usuario según los datos ingresados en el request de login
    user = db.query(User).filter(User.username == login_request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    # Verificar la contraseña según los datos ingresados en el request de login
    if not verify_password(login_request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    # Crea el token JWT
    token = create_access_token(data={"sub": user.id})
    return {"access_token": token, "token_type": "bearer"}
