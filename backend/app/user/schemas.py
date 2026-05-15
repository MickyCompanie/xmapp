from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.user.model import UserRole

class UserBase(BaseModel):
    email: EmailStr 

class UserCreate(UserBase):
    email: EmailStr
    password: str = Field(..., min_length=8) 
    first_name: str
    last_name: str

class UserUpdate(BaseModel):
    id: int
    email: EmailStr

class UserRead(UserBase):
    id: int
    is_active: bool
    role: UserRole
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserDelete(BaseModel):
    id: int 