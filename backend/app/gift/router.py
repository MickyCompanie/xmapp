from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.gift.model import Gift
from app.gift.schemas import GiftRead, GiftCreate, GiftUpdate
from app.gift import services as gift_service
from app.user.model import User, UserRole
from app.auth.depedencies import must_be_authenticated, get_current_user

gift_router = APIRouter()

@gift_router.get('/', response_model=list[GiftRead], status_code=status.HTTP_200_OK)
def get_all_gifts(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return gift_service.get_all_gifts(db, user)


@gift_router.get('/{gift_id}', dependencies=[Depends(must_be_authenticated)], response_model=GiftRead, status_code=status.HTTP_200_OK)
def get_gift_by_id(gift_id: int, db: Session = Depends(get_db)):
    return gift_service.get_gift_by_id(db, gift_id)

@gift_router.post('/', response_model=GiftRead, status_code=status.HTTP_201_CREATED)
def create_gift(gift_in: GiftCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return gift_service.create_gift(db, gift_in, user.person_id)

@gift_router.post('/{wish_id}', response_model=GiftRead, status_code=status.HTTP_201_CREATED)
def create_gift_from_wish(gift_in: GiftCreate, wish_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return gift_service.create_gift_from_wish(db, gift_in, wish_id, user.person_id)

@gift_router.put('/{gift_id}', dependencies=[Depends(must_be_authenticated)], response_model=GiftRead, status_code=status.HTTP_200_OK)
def update_gift(gift_id: int, gift_in: GiftUpdate, db: Session = Depends(get_db)):
    return gift_service.update_gift(db, gift_in, gift_id)

@gift_router.delete('/{gift_id}', dependencies=[Depends(must_be_authenticated)], status_code=status.HTTP_200_OK)
def delete_gift(gift_id: int, db: Session = Depends(get_db)):
    return gift_service.delete_gift(db, gift_id)