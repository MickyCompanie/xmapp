from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from app.db import Base
from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as EnumSQL, func, ForeignKey, String, Text
from datetime import datetime

if TYPE_CHECKING:
    from app.person.model import Person

class Wish(Base):
    __tablename__ = 'wishes'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    url: Mapped[Optional[str]] = mapped_column(String(500))
    price_estimate: Mapped[Optional[float]] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    
    
    person_id: Mapped[int] = mapped_column(ForeignKey("people.id"), nullable=False)
    owner: Mapped["Person"] = relationship(back_populates="wishes")