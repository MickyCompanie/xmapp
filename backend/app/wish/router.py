from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.wish.model import Wish
from app.wish.schemas import WishRead, WishCreate, WishUpdate
from app.wish import services as wish_service
from app.user.model import User
from app.auth.depedencies import must_be_authenticated, get_current_user

wish_router = APIRouter()

@wish_router.get('/', dependencies=[Depends(must_be_authenticated)], response_model=list[WishRead], status_code=status.HTTP_200_OK)
def get_all_wishes(db: Session = Depends(get_db)):
    return wish_service.get_all_wishes(db)

@wish_router.get('/{wish_id}', dependencies=[Depends(must_be_authenticated)], response_model=WishRead, status_code=status.HTTP_200_OK)
def get_wish_by_id(wish_id: int, db: Session = Depends(get_db)):
    return wish_service.get_wish_by_id(db, wish_id)

@wish_router.post('/', response_model=WishRead, status_code=status.HTTP_201_CREATED)
def create_wish(wish_in: WishCreate, current_user: User = Depends(get_current_user) , db: Session = Depends(get_db)):
    return wish_service.create_wish(db, wish_in, current_user.person_id)

@wish_router.put('/{wish_id}', dependencies=[Depends(must_be_authenticated)], response_model=WishRead, status_code=status.HTTP_200_OK)
def update_wish(wish_id: int, wish_in: WishUpdate, db: Session = Depends(get_db)):
    return wish_service.update_wish(db, wish_in, wish_id)

@wish_router.delete('/{wish_id}', dependencies=[Depends(must_be_authenticated)], status_code=status.HTTP_200_OK)
def delete_wish(wish_id: int, db: Session = Depends(get_db)):
    return wish_service.delete_wish(db, wish_id)