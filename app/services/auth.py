from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

from app.config.database import get_db
from app.models.user_model import User


load_dotenv()

# Configuración de encriptación de contraseña
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración JWT
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("DEBUG:: SECRET_KEY nno está en .env")

print(f"DEBUG: SECRET_KEY en auth.py: {SECRET_KEY}")

ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Hashear la contraseña
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# Verificar la contraseña
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Función creadora de token JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})

    if "sub" not in to_encode:
        raise ValueError("El token debe contener el campo 'sub' con el ID del usuario")

    to_encode["sub"] = str(to_encode["sub"])

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(f"DEBUG: Token generado: {encoded_jwt}")
    return encoded_jwt


# Obtener usuario logeado a partir del token
def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        # Aseguro que user_id sea entero
        user_id = int(user_id)

        print(f"DEBUG: user_id entero: {user_id}")

    except (JWTError, ValueError) as e:
        print(f"DEBUG: Error al decodificar token: {e}")
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user
