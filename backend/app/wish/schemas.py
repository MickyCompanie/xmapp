from app.wish.model import Wish
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional
from datetime import datetime

class WishCreate(BaseModel):
    title: str
    description: str | None = None
    url: str
    price_estimate: float

class WishUpdate(BaseModel):
    id: int
    title: str | None = None
    description: str | None = None
    url: str | None = None
    price_estimate: float | None = None


class WishRead(BaseModel):
    id: int
    title: str
    description: str
    url: str
    price_estimate: float
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)