from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt

# Configuración encriptación contraseña
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# configuración JWT
SECRET_KEY = "your_secret_key_here"  # Usa una clave segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Hashear la contraseña
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verificar la contraseña
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Funcion creadora de token JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
