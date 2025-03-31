from pydantic import BaseModel
from typing import Optional



class NoteCreate(BaseModel):
    title: str
    content: str
    version: Optional[int] = None



class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    version: int

    class Config:
        from_attributes = True
