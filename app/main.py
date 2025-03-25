from fastapi import FastAPI
from app.config.database import init_db
from app.routers import user_router

app = FastAPI()

# Creo las tablas si no existen al iniciar el backend
init_db()

app.include_router(user_router.router)

@app.get('/')
def home():
    return {"message": "Hola mundo!"}
