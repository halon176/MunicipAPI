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
