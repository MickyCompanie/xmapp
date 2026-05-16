from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime
from app.gift.model import GiftStatus

class GiftCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, examples=["Playstation"])
    price_paid: Optional[float] 
    receiver_id: int 
    status: GiftStatus 

class GiftUpdate(BaseModel):
    id: int
    title: str = Field(..., min_length=1, max_length=100, examples=["Playstation"])
    price_paid: Optional[float] 
    status: GiftStatus 

class GiftRead(BaseModel):
    id: int
    title: str = Field(..., min_length=1, max_length=100, examples=["Playstation"])
    price_paid: Optional[float] 
    giver_id: int 
    receiver_id: int 
    wish_id: Optional[int]  = None
    status: GiftStatus 
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)