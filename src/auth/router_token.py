import os
import secrets
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import APIKeyHeader

from src.auth.models import APIKey, JWTBearer

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
async def create_token():
    token = secrets.token_urlsafe(16)
    await APIKey.objects.create(apikey=token, user_id="5dcd3d226c9a4016a98d02110c3edc39", created_at=datetime.now())

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
