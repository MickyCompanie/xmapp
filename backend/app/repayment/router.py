from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.repayment.model import Repayment
from app.repayment.schemas import RepaymentRead, RepaymentCreate, RepaymentUpdate
from app.repayment import services as repayment_service
from app.user.model import User, UserRole
from app.auth.depedencies import must_be_authenticated, get_current_user, authorized_role

repayment_router = APIRouter()

@repayment_router.get('/', response_model=list[RepaymentRead], status_code=status.HTTP_200_OK)
def get_all_repayments(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return repayment_service.get_all_repayments(db, current_user)

@repayment_router.get('/{repayment_id}', dependencies=[Depends(must_be_authenticated)], response_model=RepaymentRead, status_code=status.HTTP_200_OK)
def get_repayment_by_id(repayment_id: int, db: Session = Depends(get_db)):
    return repayment_service.get_repayment_by_id(db, repayment_id)

@repayment_router.post('/', response_model=RepaymentRead, status_code=status.HTTP_201_CREATED)
def create_repayment(repayment_in: RepaymentCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return repayment_service.create_repayment(db, repayment_in)

@repayment_router.put('/{repayment_id}', response_model=RepaymentRead, status_code=status.HTTP_200_OK)
def update_repayment(repayment_id: int, repayment_in: RepaymentUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return repayment_service.update_repayment(db, repayment_in, repayment_id, current_user)

@repayment_router.delete('/{repayment_id}', status_code=status.HTTP_200_OK)
def delete_repayment(repayment_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return repayment_service.delete_repayment(db, repayment_id, current_user)