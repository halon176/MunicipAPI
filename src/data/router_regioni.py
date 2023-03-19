from typing import List

from fastapi import APIRouter

from src.data.models import Regioni

router = APIRouter(
    prefix="/regioni",
    tags=["Regioni"]
)


@router.get("/", response_model=List[Regioni])
async def list_regioni():
    regioni = await Regioni.objects.all()
    return regioni
