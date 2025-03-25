from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserCreateResponse
from app.config.database import get_db
from app.services.auth import hash_password

router = APIRouter()

# Endpoint para registrar un nuevo usuario
@router.post("/register", response_model=UserCreateResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar si el correo electrónico ya está registrado
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Verifico si el nombre de usuario ya se encuentra en la base de datos
    existing_username = db.query(User).filter(User.username == user.username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    # Creo el nuevo usuario con hash
    hashed_password = hash_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Devuelvo el usuario creado con datos relevantes, omitiendo la contraseña, por seguridad
    return UserCreateResponse(username=new_user.username, email=new_user.email)
