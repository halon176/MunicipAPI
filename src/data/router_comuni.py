from fastapi import APIRouter

from src.data.models import Regioni, Province, Comuni

router = APIRouter(
    prefix="/comuni",
    tags=["Comuni"]
)


@router.get("/{CAP}")
async def get_comune(CAP: int):
    comune = await Comuni.objects.get(CAP=CAP)
    return comune