from sqlalchemy.orm import Session
from app.gift.model import Gift, GiftStatus
from app.gift.schemas import GiftCreate, GiftUpdate, GiftRead
from fastapi import HTTPException, status
from app.user.model import User, UserRole
from app.wish.model import Wish

def get_all_gifts(db: Session, user: User) -> list[GiftRead]:
    if user.role == UserRole.SANTA:
        return db.query(Gift).all()
    return db.query(Gift).filter(Gift.giver_id == user.person_id)

def get_gift_by_id(db: Session, gift_id: str) -> GiftRead:
    gift = db.query(Gift).filter(Gift.id == gift_id).first()
    if not gift: 
        raise HTTPException(status_code=404, detail="Gift not found")
    return gift

def create_gift(db: Session, gift_in: GiftCreate, person_id: int) -> GiftRead:
    gift_data = gift_in.model_dump()

    new_gift = Gift(
        **gift_data, 
        giver_id=person_id,
    )

    db.add(new_gift)
    db.commit()
    db.refresh(new_gift)

    return new_gift

def create_gift_from_wish(db: Session, wish_id: int, person_id: int) -> Gift:
    wish = db.query(Wish).filter(Wish.id == wish_id).first()
    if not wish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Souhait introuvable."
        )

    if wish.person_id == person_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Vous ne pouvez pas créer un cadeau depuis votre propre liste de souhaits."
        )

    new_gift = Gift(
        title=wish.title,
        price_paid=wish.price_estimate,
        giver_id=person_id,
        receiver_id=wish.person_id,
        wish_id=wish.id,
        status=GiftStatus.PENDING
    )

    db.add(new_gift)
    db.commit()
    db.refresh(new_gift)

    return new_gift

def update_gift(db: Session, gift_in: GiftUpdate, gift_id: int) -> GiftRead:
    if gift_id != gift_in.id:
        raise HTTPException(status_code=400, detail="Bad id provided")
    
    db_gift = db.query(Gift).filter(Gift.id == gift_in.id).first()
    if not db_gift:
        raise HTTPException(status_code=404, detail="Gift not found")
    
    update_data = gift_in.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_gift, key, value)

    db.add(db_gift)
    db.commit()
    db.refresh(db_gift)
    
    return db_gift

def delete_gift(db: Session, gift_id: int) -> bool:
    db_gift = db.query(Gift).filter(Gift.id == gift_id).first()
    if not db_gift:
        raise HTTPException(status_code=404, detail="Gift not found")
    
    db.delete(db_gift)
    db.commit()

    return True
    