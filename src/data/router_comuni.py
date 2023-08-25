from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.router_token import api_key_auth
from src.data.models import Comune
from src.data.schemas import ComuneResponse
from src.database import get_async_session

router = APIRouter(
    prefix="/comuni",
    tags=["Comuni"],
    dependencies=[Depends(api_key_auth)]
)


@router.get("/", response_model=List[ComuneResponse])
@cache(expire=60)
async def list_comuni(session: AsyncSession = Depends(get_async_session)):
    query = select(Comune)
    comuni_obj_list = (await session.scalars(query)).all()
    return comuni_obj_list


@router.get("/{CAP}", response_model=List[ComuneResponse])
@cache(expire=60)
async def get_cap(cap: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Comune).join(Comune.provincia).where(Comune.CAP == cap)
    comuni_list = (await session.scalars(query)).all()
    comuni_list = [comune.to_json() for comune in comuni_list]
    return comuni_list


@router.get("/ricerca_comune/{nome}")
@cache(expire=60)
async def get_comune(nome: str, session: AsyncSession = Depends(get_async_session)):
    query = select(Comune).where(Comune.nome.ilike(f"%{nome}%"))
    comuni_list = (await session.scalars(query)).all()
    comuni_list = [comune.to_json() for comune in comuni_list]
    return comuni_list
