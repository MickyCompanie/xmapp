from __future__ import annotations
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Union, List
from datetime import datetime
from app.repayment.model import RepaymentStatus
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.app.expense.schemas import ExpenseRead



class RepaymentRead(BaseModel):
    id: int
    amount_to_pay: float
    status: Union[RepaymentStatus, str]
    expense_id: int
    debtor_id: int


    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class RepaymentCreate(BaseModel):
    expense_id: int
    debtor_id: int
    amount_to_pay: float = Field(..., gt=0)
    status: Optional[Union[RepaymentStatus, str]] = RepaymentStatus.PENDING

class RepaymentUpdate(BaseModel):
    id: Optional[int] = None
    expense_id: Optional[int] = None
    debtor_id: Optional[int] = None
    amount_to_pay: Optional[float] = Field(None, gt=0)
    status: Optional[Union[RepaymentStatus, str]] = None

class RepaymentCreateInExpense(BaseModel):
    amount_to_pay: float
    status: Optional[RepaymentStatus]
    debtor_id: int
