from fastapi import FastAPI
from app.config.database import init_db
from app.routers import (
    user_router,
    auth_router,
    notes_router,
)

app = FastAPI()


init_db()

# Routers
app.include_router(user_router.router)
app.include_router(auth_router.router, prefix="/api/auth", tags=["auth"])
app.include_router(notes_router.router, prefix="/api/notes", tags=["notes"])


@app.get("/")
def home():
    return {"message": "Hola mundo!"}
