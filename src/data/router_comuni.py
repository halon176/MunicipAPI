from typing import List

from fastapi import APIRouter, Depends

from src.auth.router_user import api_key_auth
from src.data.models import Comuni, GetComuni

router = APIRouter(
    prefix="/comuni",
    tags=["Comuni"],
    dependencies=[Depends(api_key_auth)]
)


@router.get("/", response_model=List[GetComuni])
async def list_comuni():
    comuni = await Comuni.objects.select_related("provincia").all()
    comuni_list = []
    for comune in comuni:
        comune_dict = comune.dict()
        comune_dict["provincia"] = comune.provincia.nome
        comuni_list.append(comune_dict)
    return comuni_list


@router.get("/{CAP}", response_model=List[GetComuni])
async def get_cap(CAP: int):
    comuni = await Comuni.objects.filter(CAP=CAP).select_related("provincia").all()
    comuni_list = []
    for comune in comuni:
        comune_dict = comune.dict()
        comune_dict["provincia"] = comune.provincia.nome
        comuni_list.append(comune_dict)
    return comuni_list


@router.get("/ricerca_comune/{nome}", response_model=List[GetComuni])
async def get_comune(nome: str):
    comuni = await Comuni.objects.filter(nome__icontains=nome).select_related("provincia").all()
    comuni_list = []
    for comune in comuni:
        comune_dict = comune.dict()
        comune_dict["provincia"] = comune.provincia.nome
        comuni_list.append(comune_dict)
    return comuni_list
