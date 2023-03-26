import os
import secrets
import uuid
from datetime import datetime

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


@router.get('/create')
async def create_token(request: Request):
    apikey = secrets.token_urlsafe(16)
    jwt_bearer = JWTBearer()
    credentials = await jwt_bearer(request)
    credentials_decoded = decodeJWT(credentials)
    credentials_decoded_uuid = uuid.UUID(credentials_decoded["user_id"])
    await APIKey.objects.create(apikey=apikey, user_id=credentials_decoded_uuid, created_at=datetime.now())
    return {"X-API-Key": apikey, "user_id": credentials_decoded["user_id"]}


@router.get('/apikey_list')
async def apikey_list(request: Request):
    jwt_bearer = JWTBearer()
    credentials = await jwt_bearer(request)
    credentials_decoded = decodeJWT(credentials)
    decoded_uuid = uuid.UUID(credentials_decoded["user_id"])
    user_apikey_list = await APIKey.objects.filter(user_id=decoded_uuid).all()
    return user_apikey_list


@router.post('/delete_apikey')
async def delete_apikey(apikey: str, request: Request):
    jwt_bearer = JWTBearer()
    credentials = await jwt_bearer(request)
    credentials_decoded = decodeJWT(credentials)
    decoded_uuid = uuid.UUID(credentials_decoded["user_id"])

    apikeys = await APIKey.objects.filter(apikey=apikey).values()
    if not apikeys:
        return f"La chiave API {apikey} non esiste nel database"

    apikey_to_delete = apikeys[0]
    if decoded_uuid == apikey_to_delete['user_id']:
        await APIKey.objects.delete(apikey=apikey)
        return f"La chiave API {apikey} è stata eliminata"
    else:
        return "La chiave API non è associata a questo utente"
