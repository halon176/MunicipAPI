from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.router_token import api_key_auth
from src.data.models import Provincia, Comune
from src.data.schemas import ProvinciaResponse, ComuneResponse
from src.database import get_async_session

router = APIRouter(
    prefix="/province",
    tags=["Province"],
    dependencies=[Depends(api_key_auth)]
)


@router.get("/", response_model=List[ProvinciaResponse])
@cache(expire=60)
async def list_province(session: AsyncSession = Depends(get_async_session)):
    query = select(Provincia)
    province_obj_list = (await session.scalars(query)).all()
    return province_obj_list


@router.get("/{nome}", response_model=List[ProvinciaResponse])
@cache(expire=60)
async def get_provincia(nome: str, session: AsyncSession = Depends(get_async_session)):
    query = select(Provincia).where(Provincia.nome.ilike(f"%{nome}%"))
    province_list = (await session.scalars(query)).all()
    return province_list


@router.get("/superficie_superiore_di/{superficie}", response_model=List[ProvinciaResponse])
@cache(expire=60)
async def superficie_superiore_di(superficie: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Provincia).where(Provincia.superficie > superficie)
    province_list = (await session.scalars(query)).all()
    return province_list


@router.get("/abitanti_superiori_a/{abitanti}", response_model=List[ProvinciaResponse])
@cache(expire=60)
async def abitanti_superiori_a(abitanti: int, session: AsyncSession = Depends(get_async_session)):
    province_obj_list = await Provincia.objects.filter(abitanti__gt=abitanti).all()
    return province_obj_list


@router.get("/r/{nome}", response_model=List[ComuneResponse])
@cache(expire=60)
async def comuni_in_provincia(nome: str, session: AsyncSession = Depends(get_async_session)):
    query = select(Comune).join(Comune.provincia).where(Provincia.nome.ilike(f"%{nome}%"))
    comuni_list = (await session.scalars(query)).all()
    comuni_list = [comune.to_json() for comune in comuni_list]
    return comuni_list
