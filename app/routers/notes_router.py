from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models.note_model import Note
from app.schemas.note_schema import (
    NoteCreate,
    NoteResponse,
)
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


# GET /api/notes/{id} - Recupero una nota por su id, siempre y cuando pertenezca a el usuario autenticado.
@router.get("/{id}", response_model=NoteResponse)
def get_note(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    note = db.query(Note).filter(Note.id == id, Note.user_id == current_user.id).first()
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return note


# PUT /api/notes/{id} - Actualizo una nota por id, debe pertenecer al usuario autenticado.
@router.put("/{id}", response_model=NoteResponse)
def update_note(
    id: int,
    note_update: NoteCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):

    note = db.query(Note).filter(Note.id == id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if note.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You cannot edit this note")

    if note.version != note_update.version:
        raise HTTPException(
            status_code=400, detail="The note has been previously modified"
        )

    note.title = note_update.title
    note.content = note_update.content
    note.version += 1

    db.commit()
    db.refresh(note)

    return note


# DELETE /api/notes/{id} - Eliminar una nota, debe pertenecer al usuario logeado.
@router.delete("/{id}", response_model=NoteResponse)
def delete_note(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    note = db.query(Note).filter(Note.id == id, Note.user_id == current_user.id).first()
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )

    db.delete(note)
    db.commit()
    return note
