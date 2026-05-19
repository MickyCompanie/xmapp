from __future__ import annotations
from enum import Enum
from datetime import datetime
from sqlalchemy import Enum as EnumSQL, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.person.model import Person
    from app.expense.model import Expense

class RepaymentStatus(Enum):
    PENDING = "pending"
    PAID = "paid"

class Repayment(Base):
    __tablename__ = "repayments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, init=False)
    amount_to_pay: Mapped[float] = mapped_column(nullable=False)


    expense_id: Mapped[int] = mapped_column(ForeignKey("expenses.id", ondelete="CASCADE"), nullable=False)
    debtor_id: Mapped[int] = mapped_column(ForeignKey("people.id"), nullable=False)

    expense: Mapped["Expense"] = relationship("Expense", back_populates="repayments")
    debtor: Mapped["Person"] = relationship("Person", foreign_keys=[debtor_id])
    status: Mapped[RepaymentStatus] = mapped_column(EnumSQL(RepaymentStatus, name='repayment_status'), default=RepaymentStatus.PENDING)
    created_at: Mapped[datetime] = mapped_column(default=func.now(), init=False)
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now(), init=False)

