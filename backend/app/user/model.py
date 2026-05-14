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

    id: Mapped[int] = mapped_column(primary_key=True, init=False)

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), init=False)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now(), init=False)

    person_id: Mapped[int] = mapped_column(ForeignKey("people.id"), nullable=False, unique=True, init=False)
    
    role: Mapped[UserRole] = mapped_column(EnumSQL(UserRole, name='user_role'), default=UserRole.USER)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    person: Mapped["Person"] = relationship(back_populates="user_account", default=None)