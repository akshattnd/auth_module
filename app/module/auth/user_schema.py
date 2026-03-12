from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    email:EmailStr
    is_active:bool
    created_at:datetime
    updated_at:datetime | None

    class Config:
        from_attributes = True
