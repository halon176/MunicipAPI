import uuid
from datetime import datetime
from typing import Optional

import bcrypt
from sqlalchemy import String, DateTime, Boolean, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class APIKey(Base):
    __tablename__ = "apikey"

    apikey: Mapped[str] = mapped_column(String(22), primary_key=True)
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID)
    ip: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(255), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    @property
    def password(self):
        raise AttributeError('La password non può essere letta')

    @password.setter
    def password(self, plaintext_password):
        self.hashed_password = bcrypt.hashpw(plaintext_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, plaintext_password):
        return bcrypt.checkpw(plaintext_password.encode('utf-8'), self.hashed_password.encode('utf-8'))

    def check_active(self):
        if self.is_active:
            return True
        else:
            return False


