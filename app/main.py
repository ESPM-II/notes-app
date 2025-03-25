from fastapi import FastAPI
from app.config.database import init_db
from app.routers import user_router, auth_router 

app = FastAPI()

#Inicializar db
init_db()

#Router de usuarios
app.include_router(user_router.router)

#Router de autenticación
app.include_router(auth_router.router, prefix="/api/auth", tags=["auth"])

@app.get('/')
def home():
    return {"message": "Hola mundo!"}
