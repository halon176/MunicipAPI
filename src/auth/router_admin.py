from typing import List

from fastapi import APIRouter, Depends, Request

from src.auth.models import JWTBearer, User
from src.auth.router_token import get_uuid_bearer

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(JWTBearer())]

)


async def verify_admin(request):
    user_uuid = await get_uuid_bearer(request)
    user = await User.objects.get(id=user_uuid)
    print(user.dict())
    if user.is_superuser:
        return True
    else:
        return False


@router.get("/im_i_admin")
async def am_i_admin(request: Request):
    is_admin = await verify_admin(request)
    return is_admin


@router.get("/user_list", response_model=List[User], response_model_exclude={"hashed_password"})
async def user_list():
    userlist = await User.objects.all()
    return userlist
