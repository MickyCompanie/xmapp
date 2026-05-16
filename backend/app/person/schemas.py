from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime


class PersonBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50, examples=["Jean"])
    last_name: str = Field(..., min_length=1, max_length=50, examples=["Dupont"])
    birth_date: datetime | None = None


class PersonCreate(PersonBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[datetime] = None


class PersonUpdate(BaseModel):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[datetime] = None
    managed_by_id: Optional[int] = None


class PersonRead(PersonBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class PersonDetail(PersonRead):
#    wishes: List["WishRead"] = [] 
    
    model_config = ConfigDict(from_attributes=True)