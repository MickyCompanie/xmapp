
from sqlalchemy.orm import Session
from app.wish.model import Wish
from app.wish.schemas import WishCreate, WishUpdate, WishRead
from app.user.model import User, UserRole
from fastapi import HTTPException


def get_all_wishes(db: Session) -> list[WishRead]:
    return db.query(Wish).all()

def get_wish_by_id(db: Session, wish_id: str) -> WishRead:
    wish = db.query(Wish).filter(Wish.id == wish_id).first()
    if not wish: 
        raise HTTPException(status_code=404, detail="Wish not found")
    return wish

def create_wish(db: Session, wish_in: WishCreate, person_id: int) -> WishRead:
    wish_data = wish_in.model_dump()

    new_wish = Wish(
        **wish_data, 
        person_id=person_id
    )

    db.add(new_wish)
    db.commit()
    db.refresh(new_wish)

    return new_wish

def update_wish(db: Session, wish_in: WishUpdate, wish_id: int, user: User) -> WishRead:
    if wish_id != wish_in.id:
        raise HTTPException(status_code=400, detail="Bad id provided")
    
    db_wish = db.query(Wish).filter(Wish.id == wish_in.id).first()
    if not db_wish:
        raise HTTPException(status_code=404, detail="Wish not found")
    
    if db_wish.person_id != user.person_id and user.role not in [UserRole.ADMIN, UserRole.SANTA]:
        raise HTTPException(status_code=403, detail="You don't have permission to update this wish")
    
    update_data = wish_in.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_wish, key, value)

    db.add(db_wish)
    db.commit()
    db.refresh(db_wish)
    
    return db_wish

def delete_wish(db: Session, wish_id: int, user: User) -> bool:
    db_wish = db.query(Wish).filter(Wish.id == wish_id).first()
    if not db_wish:
        raise HTTPException(status_code=404, detail="Wish not found")
    
    if db_wish.person_id != user.person_id and user.role not in [UserRole.ADMIN, UserRole.SANTA]:
        raise HTTPException(status_code=403, detail="You don't have permission to delete this wish")
    
    db.delete(db_wish)
    db.commit()

    return True
    