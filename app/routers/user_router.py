from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserCreateResponse
from app.config.database import get_db
from app.services.auth import hash_password

router = APIRouter()

# Endpoint para registrar usuario
@router.post("/register", response_model=UserCreateResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verifico si el correo electrónico ya está registrado
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Verifico si el nombre de usuario ya está en la base de datos
    existing_username = db.query(User).filter(User.username == user.username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
        )

    # Hash de la contraseña y creación del nuevo usuario
    hashed_password = hash_password(user.password)
    new_user = User(
        username=user.username, email=user.email, hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Devuelvo el usuario creado, omitiendo la contraseña
    return UserCreateResponse(username=new_user.username, email=new_user.email)
