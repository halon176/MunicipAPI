from typing import List
from fastapi_cache.decorator import cache

from fastapi import APIRouter, Depends

from src.auth.router_token import api_key_auth
from src.data.models import Comuni, GetComuni

router = APIRouter(
    prefix="/comuni",
    tags=["Comuni"],
    dependencies=[Depends(api_key_auth)]
)


@router.get("/", response_model=List[GetComuni])
@cache(expire=60)
async def list_comuni():
    comuni_obj_list = await Comuni.objects.select_related("provincia_id").all()
    comuni_list = []
    for comune in comuni_obj_list:
        comune_dict = comune.dict()
        comune_dict["provincia"] = comune.provincia_id.nome
        comuni_list.append(comune_dict)
    return comuni_list


@router.get("/{CAP}", response_model=List[GetComuni])
@cache(expire=60)
async def get_cap(CAP: int):
    comuni_obj_list = await Comuni.objects.filter(CAP=CAP).select_related("provincia_id").all()
    comuni_list = []
    for comune in comuni_obj_list:
        comune_dict = comune.dict()
        comune_dict["provincia"] = comune.provincia_id.nome
        comuni_list.append(comune_dict)
    return comuni_list


@router.get("/ricerca_comune/{nome}", response_model=List[GetComuni])
@cache(expire=60)
async def get_comune(nome: str):
    comuni_obj_list = await Comuni.objects.filter(nome__icontains=nome).select_related("provincia_id").all()
    comuni_list = []
    for comune in comuni_obj_list:
        comune_dict = comune.dict()
        comune_dict["provincia"] = comune.provincia_id.nome
        comuni_list.append(comune_dict)
    return comuni_list
