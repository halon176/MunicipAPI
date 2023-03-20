from typing import List

from fastapi import APIRouter

from src.data.models import Comuni, GetComuni

router = APIRouter(
    prefix="/comuni",
    tags=["Comuni"]
)


@router.get("/{CAP}", response_model=List[GetComuni])
async def get_cap(CAP: int):
    comuni = await Comuni.objects.filter(CAP=CAP).select_related("provincia").all()
    comuni_list = []
    for comune in comuni:
        comune_dict = comune.dict()
        comune_dict["provincia"] = comune.provincia.nome
        comuni_list.append(comune_dict)
    return comuni_list
