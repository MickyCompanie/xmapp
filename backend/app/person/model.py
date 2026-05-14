from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from app.db import Base
from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as EnumSQL, ForeignKey, func, String
from datetime import datetime

if TYPE_CHECKING:
    from app.user.model import User
    from app.wish.model import Wish
    from app.gift.model import Gift


class Person(Base):
    __tablename__ = 'people'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    birth_date: Mapped[Optional[datetime]] = mapped_column(nullable=True, default=None)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), init=False)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now(), init=False)

    user_account: Mapped[Optional["User"]] = relationship(back_populates="person", uselist=False, default=None)
    wishes: Mapped[list["Wish"]] = relationship(
        back_populates="owner", 
        cascade="all, delete-orphan", 
        default_factory=list
        )

    gifts_given: Mapped[list["Gift"]] = relationship(
        "Gift", 
        foreign_keys="[Gift.giver_id]", 
        back_populates="giver", 
        default_factory=list
    )
    gifts_received: Mapped[list["Gift"]] = relationship(
        "Gift", 
        foreign_keys="[Gift.receiver_id]", 
        back_populates="receiver", 
        default_factory=list
    )