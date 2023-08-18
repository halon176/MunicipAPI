from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.router_token import api_key_auth
from src.data.models import Provincia, Comune
from src.data.schemas import GetProvince, GetComuni
from src.database import get_async_session

router = APIRouter(
    prefix="/province",
    tags=["Province"],
    dependencies=[Depends(api_key_auth)]
)


@router.get("/", response_model=List[GetProvince])
@cache(expire=60)
async def list_province(session: AsyncSession = Depends(get_async_session)):
    query = select(Provincia)
    province_obj_list = (await session.scalars(query)).all()
    return province_obj_list


@router.get("/{nome}/", response_model=List[GetProvince])
@cache(expire=60)
async def get_provincia(nome: str):
    province_obj_list = await Provincia.objects.filter(nome__icontains=nome).all()
    return province_obj_list


@router.get("/superficie_superiore_di/{superficie}/", response_model=List[GetProvince])
@cache(expire=60)
async def superficie_superiore_di(superficie: int):
    province_obj_list = await Provincia.objects.filter(superficie__gt=superficie).all()
    return province_obj_list


@router.get("/abitanti_superiori_a/{abitanti}/", response_model=List[GetProvince])
@cache(expire=60)
async def abitanti_superiori_a(abitanti: int):
    province_obj_list = await Provincia.objects.filter(abitanti__gt=abitanti).all()
    return province_obj_list


@router.get("/r/{nome}/", response_model=List[GetComuni])
@cache(expire=60)
async def comuni_in_provincia(nome: str):
    province_obj_list = await Provincia.objects.filter(nome__icontains=nome).all()
    comuni_list = []
    for provincia in province_obj_list:
        comuni = await Comune.objects.filter(provincia_id=provincia.id).all()
        for comune in comuni:
            comune_dict = comune.dict()
            comune_dict["provincia"] = provincia.nome
            comuni_list.append(comune_dict)
    return comuni_list
