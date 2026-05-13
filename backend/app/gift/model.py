from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from app.db import Base
from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as EnumSQL, func, ForeignKey, String, Text
from datetime import datetime

if TYPE_CHECKING:
    from app.person.model import Person
    from app.wish import Wish

class GiftStatus(Enum):
    PENDING = "pending"
    RESERVED = "reserved"
    BOUGHT = "bought"
    WRAPPED = "wrapped"
    UNDER_TREE = "under_tree"
    GIVEN = "given"

class Gift(Base):
    __tablename__ = 'gifts'

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    price_paid: Mapped[Optional[float]] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    
    giver_id: Mapped[int] = mapped_column(ForeignKey("people.id"), nullable=False)
    receiver_id: Mapped[int] = mapped_column(ForeignKey("people.id"), nullable=False)
    wish_id: Mapped[Optional[int]] = mapped_column(ForeignKey("wishes.id"), nullable=True)

   
    giver: Mapped["Person"] = relationship("Person", foreign_keys=[giver_id], back_populates="gifts_given")
    receiver: Mapped["Person"] = relationship("Person", foreign_keys=[receiver_id], back_populates="gifts_received")
    wish: Mapped[Optional["Wish"]] = relationship("Wish")
    status: Mapped[GiftStatus] = mapped_column(EnumSQL(GiftStatus, name='gift_status'), default=GiftStatus.PENDING)