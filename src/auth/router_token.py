import os
import secrets
import uuid
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import APIKeyHeader
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.logic import decodeJWT, is_valid_ip_address, JWTBearer
from src.auth.models import APIKey
from src.database import get_async_session

router = APIRouter(
    prefix="/token",
    tags=["Token"],
    dependencies=[Depends(JWTBearer())]
)
X_API_KEY = APIKeyHeader(name='X-API-Key')


async def api_key_auth(request: Request, x_api_key: str = Depends(X_API_KEY),
                       session: AsyncSession = Depends(get_async_session)):
    query = select(APIKey).where(APIKey.apikey == x_api_key)
    apikey = (await session.scalars(query)).first()
    os.environ['API-KEY'] = apikey.apikey
    if apikey.ip is not None and apikey.ip != read_host(request):
        raise HTTPException(
            status_code=401,
            detail="Indirizzo ip da cui si sta cercando di utilizzare api non è associato ad essa"
        )
    if not apikey:
        raise HTTPException(
            status_code=401,
            detail="API Key non valida"
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


@router.post('/create')
async def create_token(request: Request, ip: Optional[str] = None, session: AsyncSession = Depends(get_async_session)):
    if ip and not is_valid_ip_address(ip):
        return {"error": "Invalid IP address"}
    apikey = secrets.token_urlsafe(16)
    uuid_user = await get_uuid_bearer(request)
    new_apikey = APIKey(apikey=apikey, user_id=uuid_user, ip=ip)
    session.add(new_apikey)
    try:
        await session.commit()
        return {"X-API-Key": apikey}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=f"Errore durante l'inserimento della chiave API: {e}")


@router.get('/apikey_list')
async def apikey_list(request: Request, session: AsyncSession = Depends(get_async_session)):
    uuid_user = await get_uuid_bearer(request)
    query = select(APIKey).where(APIKey.user_id == uuid_user)
    user_apikey_list = (await session.scalars(query)).all()
    return user_apikey_list


@router.post('/delete_apikey')
async def delete_apikey(apikey: str, request: Request, session: AsyncSession = Depends(get_async_session)):
    uuid_user = await get_uuid_bearer(request)
    query = select(APIKey).where(APIKey.apikey == apikey)
    apikey_to_delete = (await session.scalars(query)).first()
    if not apikey_to_delete:
        return f"La chiave API {apikey} non esiste nel database"
    if uuid_user != apikey_to_delete.user_id:
        return "La chiave API non è associata a questo utente"
    else:
        await session.execute(delete(APIKey).where(APIKey.apikey == apikey))
        await session.commit()
        return f"La chiave API {apikey} è stata eliminata"
