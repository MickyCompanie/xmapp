from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.user.model import User
from app.user.schemas import UserRead, UserCreate, UserUpdate
from app.user import services as user_service
from app.auth.depedencies import get_current_user


user_router = APIRouter()

@user_router.post('/signup', response_model=UserRead, status_code=status.HTTP_201_CREATED)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is already used."
        )
    
    new_user = user_service.create_user(db=db, user_in=user_in)
    return new_user

@user_router.get("/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user