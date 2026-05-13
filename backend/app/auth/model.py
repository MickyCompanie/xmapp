from __future__ import annotations
from typing import TYPE_CHECKING
from app.db import Base
from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as EnumSQL, ForeignKey, func, String
from datetime import datetime

if TYPE_CHECKING:
    from app.person.model import Person

class UserRole(Enum):
    USER = 'user'
    ADMIN = 'admin'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    person_id: Mapped[int] = mapped_column(ForeignKey("people.id"), nullable=False, unique=True)
    person: Mapped["Person"] = relationship(back_populates="user_account")
    
    role: Mapped[UserRole] = mapped_column(EnumSQL(UserRole, name='user_role'), default=UserRole.USER)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)