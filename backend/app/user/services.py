from sqlalchemy.orm import Session
from app.user.model import User
from app.user.schemas import UserCreate
from app.person.model import Person
from app.auth.utils import hash_password

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user_in: UserCreate):
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
    
    # SQLAlchemy va comprendre qu'il doit d'abord insérer Person, récupérer l'ID, et le mettre dans User automatiquement.
    db.commit()
    
    db.refresh(new_user)
    return new_user