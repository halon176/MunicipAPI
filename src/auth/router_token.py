import os
import secrets
import uuid
from datetime import datetime
from typing import Dict, List

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import APIKeyHeader

from src.auth.logic import decodeJWT
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


async def get_uuid_bearer(request) -> uuid.UUID:
    jwt_bearer = JWTBearer()
    credentials = await jwt_bearer(request)
    credentials_decoded = decodeJWT(credentials)
    credentials_decoded_uuid = uuid.UUID(credentials_decoded["user_id"])
    return credentials_decoded_uuid

@router.get("/")
def read_host(request: Request):
    client_host = request.client.host
    return client_host


@router.get('/create', response_model=Dict[str, str])
async def create_token(request: Request):
    apikey = secrets.token_urlsafe(16)
    uuid_user = await get_uuid_bearer(request)
    await APIKey.objects.create(apikey=apikey, user_id=uuid_user, created_at=datetime.now())
    return {"X-API-Key": apikey, "user_id": uuid_user}


@router.get('/apikey_list', response_model=List[APIKey])
async def apikey_list(request: Request):
    uuid_user = await get_uuid_bearer(request)
    user_apikey_list = await APIKey.objects.filter(user_id=uuid_user).all()
    return user_apikey_list


@router.post('/delete_apikey')
async def delete_apikey(apikey: str, request: Request):
    uuid_user = await get_uuid_bearer(request)
    apikey_to_delete = await APIKey.objects.filter(apikey=apikey).get_or_none()
    if not apikey_to_delete:
        return f"La chiave API {apikey} non esiste nel database"
    if uuid_user != apikey_to_delete.user_id:
        return "La chiave API non è associata a questo utente"
    else:
        await APIKey.objects.delete(apikey=apikey)
        return f"La chiave API {apikey} è stata eliminata"
