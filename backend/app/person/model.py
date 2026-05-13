from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from app.db import Base
from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as EnumSQL, ForeignKey, func, String
from datetime import datetime

if TYPE_CHECKING:
    from app.auth.model import User
    from app.wish.model import Wish


class Person(Base):
    __tablename__ = 'people'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    birth_date: Mapped[datetime] = mapped_column()

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    user_account: Mapped[Optional["User"]] = relationship(back_populates="person", uselist=False)
    wishes: Mapped[list["Wish"]] = relationship(back_populates="owner", cascade="all, delete-orphan")