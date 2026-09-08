from __future__ import annotations
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime
from app.expense.model import ExpenseStatus, ExpenseType
from app.repayment.schemas import RepaymentRead, RepaymentCreateInExpense



class ExpenseRead(BaseModel):
    id: int
    title: str
    total_amount: float
    expense_type: ExpenseType
    status: ExpenseStatus
    is_shared: bool

    repayments: Optional[list[RepaymentRead]]

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ExpenseCreate(BaseModel):
    title: str
    total_amount: float
    expense_type: Optional[ExpenseType]
    status: Optional[ExpenseStatus]
    is_shared: bool

    repayments: Optional[list[RepaymentCreateInExpense]] = []

class ExpenseUpdate(BaseModel):
    id: int
    title: str
    total_amount: float
    expense_type: Optional[ExpenseType]
    status: Optional[ExpenseStatus]
    is_shared: bool

    repayments: Optional[list[RepaymentRead]]


ExpenseRead.model_rebuild()
ExpenseCreate.model_rebuild()
ExpenseUpdate.model_rebuild()