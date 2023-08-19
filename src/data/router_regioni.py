from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.router_token import api_key_auth
from src.data.models import Regione
from src.data.schemas import RegioneResponse
from src.database import get_async_session

router = APIRouter(
    prefix="/regioni",
    tags=["Regioni"],
    dependencies=[Depends(api_key_auth)]

)


@router.get("/", response_model=List[RegioneResponse])
@cache(expire=60)
async def list_regioni(session: AsyncSession = Depends(get_async_session)):
    query = select(Regione)
    regioni = (await session.scalars(query)).all()
    return regioni


@router.get("/superficie_superiore_di/{superficie}", response_model=List[RegioneResponse])
@cache(expire=60)
async def superficie_superiore_di(superficie: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Regione).where(Regione.superficie > superficie)
    regioni = (await session.scalars(query)).all()
    return regioni


@router.get("/abitanti_superiori_a/{abitanti}", response_model=List[RegioneResponse])
@cache(expire=60)
async def abitanti_superiori_a(abitanti: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Regione).where(Regione.abitanti > abitanti)
    regioni = (await session.scalars(query)).all()
    return regioni
