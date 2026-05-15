from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.user.model import User
from app.user.schemas import UserRead, UserCreate, UserUpdate, UserDelete
from app.user import services as user_service
from app.auth.depedencies import must_be_authenticated, get_current_user


user_router = APIRouter()

@user_router.post('/signup', response_model=UserRead, status_code=status.HTTP_201_CREATED)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    return user_service.signup(db=db, user_in=user_in)

@user_router.get("/me", response_model=UserRead, status_code=status.HTTP_200_OK)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@user_router.get("/", dependencies=[Depends(must_be_authenticated)], response_model=list[UserRead], status_code=status.HTTP_200_OK)
def get_all_users(db: Session = Depends(get_db)):
    return user_service.get_all_users(db)

@user_router.put("/{id}", dependencies=[Depends(must_be_authenticated)], response_model=UserRead, status_code=status.HTTP_200_OK)
def update_user(id: int, user_in: UserUpdate, db: Session = Depends(get_db)):
    return user_service.update_user(db, user_in, id)

@user_router.delete("/{id}", dependencies=[Depends(must_be_authenticated)], response_model=UserRead, status_code=status.HTTP_200_OK)
def delete_user(id: int, user_in: UserDelete, db: Session = Depends(get_db)):
    return user_service.delete_user(db, user_in, id)

@user_router.post("/reactivate/{id}", dependencies=[Depends(must_be_authenticated)], response_model=UserRead, status_code=status.HTTP_200_OK)
def delete_user(id: int, user_in: UserDelete, db: Session = Depends(get_db)):
    return user_service.reactivate_user(db, user_in, id)