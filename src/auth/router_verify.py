import os

from fastapi import APIRouter, Depends, Request
from fastapi.security import APIKeyHeader
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import APIKey
from src.auth.router_token import read_host
from src.database import get_async_session

router = APIRouter(
    prefix="/verify",
    tags=["Verify"],
)

X_API_KEY = APIKeyHeader(name='X-API-Key')


@router.get("/")
async def verify_apikey(request: Request, x_api_key: str = Depends(X_API_KEY),
                        session: AsyncSession = Depends(get_async_session)):
    query = select(APIKey).where(APIKey.apikey == x_api_key)
    apikey = (await session.scalars(query)).first()
    if not apikey:
        return False
    else:
        os.environ['API-KEY'] = apikey.apikey
        if apikey.ip and apikey.ip != read_host(request):
            return False
        else:
            return True
