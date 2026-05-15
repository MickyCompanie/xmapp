from sqlalchemy.orm import Session
from app.user.model import User
from app.user.schemas import UserCreate, UserUpdate
from app.person.model import Person
from app.auth.utils import hash_password
from fastapi import HTTPException

def get_all_users(db: Session):
    return db.query(User).filter(User.is_active == True).all()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def signup(db: Session, user_in: UserCreate):    
    db_user = get_user_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(status_code=400, detail="This email is already used.")

    new_person = Person(
        first_name=user_in.first_name, 
        last_name=user_in.last_name
    )
    db.add(new_person)

    
    new_user = User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        person=new_person,  
        is_active=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def update_user(db: Session, user_in: UserUpdate, id: int):
    if id != user_in.id:
        raise HTTPException(status_code=404, detail="bad id provided")
    
    db_user = db.query(User).filter(User.id == user_in.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user.email = user_in.email

    db.add(db_user)
    db.commit()
    
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_in: UserUpdate, id: int):
    if id != user_in.id:
        raise HTTPException(status_code=404, detail="bad id provided")
    
    db_user = db.query(User).filter(User.id == user_in.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user.is_active = False

    db.add(db_user)
    db.commit()
    
    db.refresh(db_user)
    return db_user

def reactivate_user(db: Session, user_in: UserUpdate, id: int):
    if id != user_in.id:
        raise HTTPException(status_code=404, detail="bad id provided")
    
    db_user = db.query(User).filter(User.id == user_in.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user.is_active = True

    db.add(db_user)
    db.commit()
    
    db.refresh(db_user)
    return db_user