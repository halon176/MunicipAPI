from typing import List

from fastapi import APIRouter

from src.data.models import Province, GetProvince

router = APIRouter(
    prefix="/province",
    tags=["Province"]
)


@router.get("/", response_model=List[GetProvince])
async def list_regioni():
    province = await Province.objects.all()
    return province


@router.get("/{nome}")
async def get_provincia(nome: str):
    province = await Province.objects.filter(nome=nome).get()
    return province
