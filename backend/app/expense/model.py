from __future__ import annotations
from enum import Enum
from datetime import datetime
from typing import List
from sqlalchemy import Enum as EnumSQL, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.person.model import Person
    from app.repayment.model import Repayment

class ExpenseType(str, Enum):
    FOOD = "food"
    DECORATION = "decoration"
    TRANSPORT = "transport"
    OTHER = "other"

class ExpenseStatus(str, Enum):
    PENDING = "pending"
    PARTIALLY_REPAID = "partially_repaid"
    FULLY_REPAID = "fully_repaid"

class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, init=False)
    title: Mapped[str] = mapped_column(nullable=False)
    total_amount: Mapped[float] = mapped_column(nullable=False)
    
    

    payer_id: Mapped[int] = mapped_column(ForeignKey("people.id"), nullable=False)
    
    payer: Mapped["Person"] = relationship("Person", foreign_keys=[payer_id])
    repayments: Mapped[List["Repayment"]] = relationship(
        "Repayment", 
        back_populates="expense", 
        cascade="all, delete-orphan"
    )
    expense_type: Mapped[ExpenseType] = mapped_column(EnumSQL(ExpenseType, name='expense_type'), default=ExpenseType.OTHER)
    status: Mapped[ExpenseStatus] = mapped_column(EnumSQL(ExpenseStatus, name='expense_status'), default=ExpenseStatus.FULLY_REPAID)
    is_shared: Mapped[bool] = mapped_column(default=False) 
    created_at: Mapped[datetime] = mapped_column(default=func.now(), init=False)
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now(), init=False)