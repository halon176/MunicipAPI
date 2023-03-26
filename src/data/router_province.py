from typing import List

from fastapi import APIRouter, Depends

from src.auth.router_user import api_key_auth
from src.data.models import Province, GetProvince, GetComuni, Comuni

router = APIRouter(
    prefix="/province",
    tags=["Province"],
    dependencies=[Depends(api_key_auth)]
)


@router.get("/", response_model=List[GetProvince])
async def list_province():
    province = await Province.objects.all()
    return province


@router.get("/{nome}", response_model=List[GetProvince])
async def get_provincia(nome: str):
    province = await Province.objects.filter(nome__icontains=nome).all()
    return province


@router.get("/superficie_superiore_di/{superficie}", response_model=List[GetProvince])
async def superficie_superiore_di(superficie: int):
    province = await Province.objects.filter(superficie__gt=superficie).all()
    return province


@router.get("/abitanti_superiori_a/{superficie}", response_model=List[GetProvince])
async def abitanti_superiori_a(abitanti: int):
    province = await Province.objects.filter(superficie__gt=abitanti).all()
    return province


@router.get("/r/{nome}", response_model=List[GetComuni])
async def comuni_in_provincia(nome: str):
    province = await Province.objects.filter(nome__iexact=nome).get()
    comuni = await Comuni.objects.filter(provincia__iexact=province.id).all()
    comuni_list = []
    for comune in comuni:
        comune_dict = comune.dict()
        comune_dict["provincia"] = province.nome
        comuni_list.append(comune_dict)
    return comuni_list
