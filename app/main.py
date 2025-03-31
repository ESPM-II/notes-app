from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.database import init_db
from app.routers import (
    user_router,
    auth_router,
    notes_router,
)

app = FastAPI()

# Activando Cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

# Inicialización de la base de datos
init_db()

# Routers
app.include_router(user_router.router, prefix="/api/user", tags=["user"])
app.include_router(auth_router.router, prefix="/api/auth", tags=["auth"])
app.include_router(notes_router.router, prefix="/api/notes", tags=["notes"])

@app.get("/")
def home():
    return {"message": "Hola mundo!"}

