from __future__ import annotations
from sqlalchemy.orm import Session
from app.expense.model import Expense, ExpenseStatus
from app.repayment.model import Repayment, RepaymentStatus
from app.expense.schemas import ExpenseCreate, ExpenseUpdate, ExpenseRead
from app.repayment import services as repayment_service
from fastapi import HTTPException
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.user.model import User


def get_all_expenses(db: Session) -> list[ExpenseRead]:
    return db.query(Expense).all()

def get_expense_by_id(db: Session, expense_id: int):
        db_expense = db.query(Expense).filter(Expense.id == expense_id).first()
        if not db_expense:
            raise HTTPException(status_code=404, detail="Expense not found")
        return db_expense

def create_expense(db: Session, expense_in: ExpenseCreate, payer_id: int):
    expense_data = expense_in.model_dump(exclude={"repayments"})
    expense = Expense(**expense_data, payer_id=payer_id)

    if expense_in.repayments:
        for rep in expense_in.repayments:
            print('-----------------ICI------------------')
            print(rep.debtor_id)
            repayment = Repayment(
                debtor_id=rep.debtor_id,
                amount_to_pay=rep.amount_to_pay,
                status=rep.status,
            )
            print(repayment)
            expense.repayments.append(repayment)

    db.add(expense)
    db.commit()
    db.refresh(expense)

    return expense

def update_expense(db: Session, expense_id: int, expense_in: ExpenseUpdate):
    # 1. Vérification de la correspondance des IDs
    if expense_in.id != expense_id:
        raise HTTPException(
            status_code=400, 
            detail="ID mismatch between URL and payload body"
        )

    # 2. Récupération de la dépense
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(
            status_code=404, 
            detail=f"Expense with id {expense_id} not found"
        )

    # 3. Mise à jour des champs
    update_data = expense_in.model_dump(exclude={"repayments"}, exclude_unset=True)
    for field, value in update_data.items():
        setattr(expense, field, value)

    db.commit()
    db.refresh(expense)
    return expense


def delete_expense(db: Session, expense_id: int):
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    db.delete(db_expense)
    db.commit()

    return True