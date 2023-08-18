from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from src.auth.router_token import api_key_auth
from src.data.models import Regione
from src.data.schemas import GetRegioni

router = APIRouter(
    prefix="/regioni",
    tags=["Regioni"],
    dependencies=[Depends(api_key_auth)]

)


@router.get("/", response_model=List[GetRegioni])
@cache(expire=60)
async def list_regioni():
    regioni = await Regione.objects.all()
    return regioni


@router.get("/superficie_superiore_di/{superficie}/", response_model=List[GetRegioni])
@cache(expire=60)
async def superficie_superiore_di(superficie: int):
    regioni = await Regione.objects.filter(superficie__gt=superficie).all()
    return regioni


@router.get("/abitanti_superiori_a/{abitanti}/", response_model=List[GetRegioni])
@cache(expire=60)
async def abitanti_superiori_a(abitanti: int):
    regioni = await Regione.objects.filter(abitanti__gt=abitanti).all()
    return regioni
