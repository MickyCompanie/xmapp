from __future__ import annotations
from typing import TYPE_CHECKING
from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.expense.model import Expense
from app.repayment.model import Repayment, RepaymentStatus
from app.repayment.schemas import RepaymentCreate, RepaymentUpdate
from app.user.model import UserRole

if TYPE_CHECKING:
    from app.user.model import User


def _check_repayment_permission(repayment: Repayment, current_user: User):
    if current_user.role in [UserRole.ADMIN, UserRole.SANTA]:
        return

    payer_id = repayment.expense.payer_id if repayment.expense else None
    if current_user.person_id in [repayment.debtor_id, payer_id]:
        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have permission to alter or delete this repayment."
    )


def get_all_repayments(db: Session, current_user: User) -> list[Repayment]:
    if current_user.role in [UserRole.ADMIN, UserRole.SANTA]:
        return db.query(Repayment).all()

    return (
        db.query(Repayment)
        .join(Expense, Repayment.expense_id == Expense.id)
        .filter(
            or_(
                Repayment.debtor_id == current_user.person_id,
                Expense.payer_id == current_user.person_id,
            )
        )
        .all()
    )


def get_repayment_by_id(db: Session, repayment_id: int) -> Repayment:
    repayment = db.query(Repayment).filter(Repayment.id == repayment_id).first()
    if not repayment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repayment Not Found"
        )
    return repayment


def create_repayment(db: Session, repayment_in: RepaymentCreate) -> Repayment:
    expense = db.query(Expense).filter(Expense.id == repayment_in.expense_id).first()
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    repayment_data = repayment_in.model_dump()
    new_repayment = Repayment(**repayment_data)

    db.add(new_repayment)
    db.commit()
    db.refresh(new_repayment)

    return new_repayment


def create_repayment_from_expense(
    db: Session,
    expense_id: int,
    debtor_id: int,
    amount_to_pay: float,
    status_val: str = None
) -> Repayment:
    new_repayment = Repayment(
        amount_to_pay=amount_to_pay,
        expense_id=expense_id,
        debtor_id=debtor_id,
        status=status_val or RepaymentStatus.PENDING
    )

    db.add(new_repayment)
    db.flush()

    return new_repayment


def update_repayment(
    db: Session,
    repayment_in: RepaymentUpdate,
    repayment_id: int,
    current_user: User
) -> Repayment:
    if repayment_in.id is not None and repayment_id != repayment_in.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad id provided"
        )

    db_repayment = db.query(Repayment).filter(Repayment.id == repayment_id).first()
    if not db_repayment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repayment Not Found"
        )

    _check_repayment_permission(db_repayment, current_user)

    if (
        current_user.person_id == db_repayment.debtor_id
        and current_user.role not in [UserRole.ADMIN, UserRole.SANTA]
    ):
        if (
            repayment_in.amount_to_pay is not None
            and repayment_in.amount_to_pay != db_repayment.amount_to_pay
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="As a debtor, you can only update the status, not the amount."
            )

    update_data = repayment_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_repayment, key, value)

    db.add(db_repayment)
    db.commit()
    db.refresh(db_repayment)

    return db_repayment


def sync_expense_repayments(db: Session, expense_id: int, repayments_data: list[dict]):
    for rep_data in repayments_data:
        if rep_data.get("id"):
            db_rep = db.query(Repayment).filter(Repayment.id == rep_data["id"]).first()
            if not db_rep:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Repayment Not Found"
                )

            for key, value in rep_data.items():
                setattr(db_rep, key, value)
        else:
            new_repayment = Repayment(
                expense_id=expense_id,
                debtor_id=rep_data["debtor_id"],
                amount_to_pay=rep_data["amount_to_pay"],
                status=rep_data.get("status") or RepaymentStatus.PENDING
            )
            db.add(new_repayment)

    db.flush()


def delete_repayment(db: Session, repayment_id: int, current_user: User) -> bool:
    db_repayment = db.query(Repayment).filter(Repayment.id == repayment_id).first()
    if not db_repayment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repayment Not Found"
        )

    _check_repayment_permission(db_repayment, current_user)

    db.delete(db_repayment)
    db.commit()

    return True