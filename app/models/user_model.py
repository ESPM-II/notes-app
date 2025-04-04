from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.config.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    notes = relationship("Note", back_populates="owner", cascade="all, delete-orphan")
