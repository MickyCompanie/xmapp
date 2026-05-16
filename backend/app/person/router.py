from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.person.model import Person
from app.person.schemas import PersonRead, PersonCreate, PersonUpdate
from app.person import services as person_service
from app.user.model import User
from app.auth.depedencies import must_be_authenticated, get_current_user

person_router = APIRouter()

@person_router.get('/', dependencies=[Depends(must_be_authenticated)], response_model=list[PersonRead], status_code=status.HTTP_200_OK)
def get_all_people(db: Session = Depends(get_db)):
    return person_service.get_all_people(db)

@person_router.get('/{person_id}', dependencies=[Depends(must_be_authenticated)], response_model=PersonRead, status_code=status.HTTP_200_OK)
def get_person_by_id(person_id: int, db: Session = Depends(get_db)):
    return person_service.get_person_by_id(db, person_id)

@person_router.post('/', dependencies=[Depends(must_be_authenticated)], response_model=PersonRead, status_code=status.HTTP_201_CREATED)
def create_person(person_in: PersonCreate, db: Session = Depends(get_db)):
    return person_service.create_person(db, person_in)

@person_router.put('/{person_id}', dependencies=[Depends(must_be_authenticated)], response_model=PersonRead, status_code=status.HTTP_200_OK)
def update_person(person_id: int, person_in: PersonUpdate, db: Session = Depends(get_db)):
    return person_service.update_person(db, person_in, person_id)

@person_router.delete('/{person_id}', dependencies=[Depends(must_be_authenticated)], status_code=status.HTTP_200_OK)
def delete_person(person_id: int, db: Session = Depends(get_db)):
    return person_service.delete_person(db, person_id)