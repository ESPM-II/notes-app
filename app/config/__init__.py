import os
from dotenv import load_dotenv


load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY", "defaultsecretkey")  # Usa la variable de entorno, si no existe usa una por defecto
ALGORITHM = os.getenv("ALGORITHM", "HS256")  # Algoritmo JWT
DATABASE_URL = os.getenv("DATABASE_URL")  # URL de la base de datos
