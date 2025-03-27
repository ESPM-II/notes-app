from pydantic import BaseModel
from typing import Optional


# Clase para crear una nueva nota
class NoteCreate(BaseModel):
    title: str
    content: str
    version: Optional[int] = None


# Clase para la respuesta de una nota
class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    version: int

    class Config:
        from_attributes = True
