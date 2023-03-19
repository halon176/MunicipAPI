from typing import List

from fastapi import APIRouter

from src.data.models import Regioni, Province, Comuni

router = APIRouter(
    prefix="/province",
    tags=["Province"]
)


@router.get("/", response_model=List[Province])
async def list_regioni():
    province = await Province.objects.all()
    return province