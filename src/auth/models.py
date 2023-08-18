import ipaddress
import uuid
from datetime import datetime
from typing import Optional

import bcrypt
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import String, DateTime, Boolean, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.auth.logic import decodeJWT
from src.database import Base


def is_valid_ip_address(ip: str) -> bool:
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


class APIKey(Base):
    __tablename__ = "apikey"

    apikey: Mapped[str] = mapped_column(String(22), primary_key=True)
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID)
    ip: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class User(Base):
    __tablename__ = "users"

    id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
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


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid
