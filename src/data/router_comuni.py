from typing import List

from fastapi import APIRouter

from src.data.models import Regioni, Province, Comuni, Get_comuni

router = APIRouter(
    prefix="/comuni",
    tags=["Comuni"]
)


@router.get("/{CAP}", response_model=List[Get_comuni])
async def get_CAP(CAP: int):
    comuni = await Comuni.objects.filter(CAP=CAP).select_related("provincia").all()
    comuni_list = []
    for comune in comuni:
        comune_dict = comune.dict()
        comune_dict["provincia"] = comune.provincia.nome
        comuni_list.append(comune_dict)
    return comuni_list


