from typing import List

from fastapi import APIRouter, Depends

from src.auth.router_user import api_key_auth
from src.data.models import Regioni, GetRegioni

router = APIRouter(
    prefix="/regioni",
    tags=["Regioni"],
    dependencies=[Depends(api_key_auth)]

)


@router.get("/", response_model=List[GetRegioni])
async def list_regioni():
    regioni = await Regioni.objects.all()
    return regioni


@router.get("/superficie_superiore_di/{superficie}", response_model=List[GetRegioni])
async def superficie_superiore_di(superficie: int):
    regioni = await Regioni.objects.filter(superficie__gt=superficie).all()
    return regioni


@router.get("/abitanti_superiori_a/{superficie}", response_model=List[GetRegioni])
async def abitanti_superiori_a(abitanti: int):
    regioni = await Regioni.objects.filter(superficie__gt=abitanti).all()
    return regioni
