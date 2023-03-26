import os
import secrets
from datetime import datetime
import ormar
import bcrypt
from email_validator import validate_email, EmailNotValidError
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import APIKeyHeader

from src.auth.models import APIKey

router = APIRouter(
    prefix="/token",
    tags=["Token"]
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

# async def api_key_auth_admin(x_api_key: str = Depends(X_API_KEY)):
#     apikey = await APIKey.objects.filter(apikey=x_api_key).get()
#     os.environ['API-KEY'] = apikey.apikey
#     if x_api_key != os.environ['API-KEY']:
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid API Key. Check that you are passing a 'X-API-Key' on your header."
#         )
#
#
