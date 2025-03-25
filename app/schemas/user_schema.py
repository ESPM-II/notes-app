from pydantic import BaseModel, EmailStr


class UserCreateResponse(BaseModel):
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    
    class Config:
        from_attributes = True
        


class UserOut(BaseModel):
    username: str
    email: EmailStr

    class Config:
        from_attributes = True
