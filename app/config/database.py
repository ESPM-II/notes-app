from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Conexión a PostgreSQL 
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:Db2025!@localhost:5432/note_app"
)

# Creo el motor de la DB
engine = create_engine(DATABASE_URL)

# Creo la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()


def init_db():
    from app.models import user_model

    Base.metadata.create_all(bind=engine)


# Función para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
