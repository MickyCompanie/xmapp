from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.expense.model import Expense
from app.expense.schemas import ExpenseRead, ExpenseCreate, ExpenseUpdate
from app.expense import services as expense_service
from app.user.model import User
from app.auth.depedencies import must_be_authenticated, get_current_user

expense_router = APIRouter()

@expense_router.get('/', dependencies=[Depends(must_be_authenticated)], response_model=list[ExpenseRead], status_code=status.HTTP_200_OK)
def get_all_expenses(db: Session = Depends(get_db)):
    return expense_service.get_all_expenses(db)

@expense_router.get('/{expense_id}', dependencies=[Depends(must_be_authenticated)], response_model=ExpenseRead, status_code=status.HTTP_200_OK)
def get_expense_by_id(expense_id: int, db: Session = Depends(get_db)):
    return expense_service.get_expense_by_id(db, expense_id)

@expense_router.post('/', response_model=ExpenseRead, status_code=status.HTTP_201_CREATED)
def create_expense(expense_in: ExpenseCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return expense_service.create_expense(db, expense_in, current_user.person_id)

@expense_router.put('/{expense_id}', dependencies=[Depends(must_be_authenticated)], response_model=ExpenseRead, status_code=status.HTTP_200_OK)
def update_expense(expense_id: int, expense_in: ExpenseUpdate, db: Session = Depends(get_db)):
    return expense_service.update_expense(db, expense_id, expense_in)

@expense_router.delete('/{expense_id}', dependencies=[Depends(must_be_authenticated)], status_code=status.HTTP_200_OK)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    return expense_service.delete_expense(db, expense_id)