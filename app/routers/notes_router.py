from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models.note_model import Note
from app.schemas.note_schema import NoteCreate, NoteResponse
from app.services.auth import get_current_user
from typing import List

router = APIRouter()


# GET /notes - Devuelvo todas las notas de usuario autenticado
@router.get("/", response_model=List[NoteResponse])
def get_notes(
    db: Session = Depends(get_db), current_user: int = Depends(get_current_user)
):
    notes = db.query(Note).filter(Note.user_id == current_user.id).all()
    return notes


# POST /notes - Creo una nueva nota (del usuario autenticado que lo solicite)
@router.post("/", response_model=NoteResponse)
def create_note(
    note_data: NoteCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    new_note = Note(
        title=note_data.title,
        content=note_data.content,
        user_id=current_user.id,
        version=1,
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note
