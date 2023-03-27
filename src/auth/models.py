import ipaddress
import uuid
from typing import Optional

import ormar
from datetime import datetime
import bcrypt
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.auth.logic import decodeJWT
from src.database import metadata, database

def is_valid_ip_address(ip: str) -> bool:
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

class APIKey(ormar.Model):
    class Meta:
        metadata = metadata
        database = database
        tablename = "apikey"

    apikey: str = ormar.String(primary_key=True, max_length=22)
    user_id: uuid.UUID = ormar.UUID(default=None)
    ip: Optional[str] = ormar.String(max_length=45, nullable=True, validators=[is_valid_ip_address])
    created_at: datetime = ormar.DateTime(default=datetime.utcnow)




class User(ormar.Model):
    class Meta:
        metadata = metadata
        database = database
        tablename = "users"

    id: uuid.UUID = ormar.UUID(primary_key=True, default=uuid.uuid4)
    username: str = ormar.String(unique=True, max_length=255)
    email: str = ormar.String(index=True, unique=True, max_length=255)
    hashed_password: str = ormar.String(max_length=255)
    is_active: bool = ormar.Boolean(default=False, nullable=False)
    is_superuser: bool = ormar.Boolean(default=False, nullable=False)
    created_at: datetime = ormar.DateTime(default=datetime.utcnow)

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
