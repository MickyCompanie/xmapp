from sqlalchemy.orm import Session
from app.person.model import Person
from app.person.schemas import PersonCreate, PersonUpdate, PersonRead
from fastapi import HTTPException


def get_all_people(db: Session) -> list[PersonRead]:
    return db.query(Person).all()

def get_person_by_id(db: Session, person_id: int) -> PersonRead:
    person = db.query(Person).filter(Person.id == person_id).first()
    if not person: 
        raise HTTPException(status_code=404, detail="Person not found")
    return person

def create_person(db: Session, person_in: PersonCreate) -> PersonRead:
    person_data = person_in.model_dump()
    new_person = Person(**person_data)

    db.add(new_person)
    db.commit()
    db.refresh(new_person)

    return new_person

def update_person(db: Session, person_in: PersonUpdate, person_id: int) -> PersonRead:
    if person_id != person_in.id:
        raise HTTPException(status_code=400, detail="Bad id provided")
    
    db_person = db.query(Person).filter(Person.id == person_in.id).first()
    if not db_person:
        raise HTTPException(status_code=404, detail="Wish not found")
    
    update_data = person_in.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_person, key, value)

    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    
    return db_person

def delete_person(db: Session, person_id: int) -> bool:
    db_person = db.query(Person).filter(Person.id == person_id).first()
    if not db_person:
        raise HTTPException(status_code=404, detail="Wish not found")
    if db_person.user_account:
        raise HTTPException(status_code=400, detail="Cannot delete a person with a user account")
    
    db.delete(db_person)
    db.commit()

    return True
    