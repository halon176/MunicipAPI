import os
import secrets
import uuid
from datetime import datetime

import jwt
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import APIKeyHeader, HTTPAuthorizationCredentials

from src.auth.logic import decodeJWT
from src.auth.models import APIKey, JWTBearer, User
from src.config import SECRET_AUTH, ALGORITHM


router = APIRouter(
    prefix="/token",
    tags=["Token"],
    dependencies=[Depends(JWTBearer())]
)

X_API_KEY = APIKeyHeader(name='X-API-Key')


async def api_key_auth(x_api_key: str = Depends(X_API_KEY)):
    apikey = await APIKey.objects.filter(apikey=x_api_key).get()
    os.environ['API-KEY'] = apikey.apikey
    if x_api_key != os.environ['API-KEY']:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key. Check that you are passing a 'X-API-Key' on your header."
        )


@router.get('/create')
async def create_token(request: Request):
    apikey = secrets.token_urlsafe(16)
    jwt_bearer = JWTBearer()
    credentials = await jwt_bearer(request)
    credentials_decoded = decodeJWT(credentials)
    user = await User.objects.get(username=credentials_decoded["user_id"])
    await APIKey.objects.create(apikey=apikey, user_id=user.id, created_at=datetime.now())
    return {"X-API-Key": apikey, "user_id": user.id}




