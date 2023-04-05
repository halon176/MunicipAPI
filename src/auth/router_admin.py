import uuid
from typing import List

from fastapi import APIRouter, Depends, Request, HTTPException
from ormar.exceptions import NoMatch

from src.auth.models import JWTBearer, User
from src.auth.router_token import get_uuid_bearer

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(JWTBearer())]

)


async def get_user_obj(user_id=uuid.UUID) -> User:
    user = await User.objects.get(id=user_id)
    return user


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


@router.post("/activate_user")
async def activate_user(user_id: uuid.UUID):
    try:
        user = await get_user_obj(user_id)
        user.is_active = True
        await user.update()
        return {"detail": f"l'utente {user.username} è stato abilitato"}
    except NoMatch:
        raise HTTPException(status_code=404, detail="L'utente specificato non esiste nel database")


@router.post("/deactivate_user")
async def deactivate_user(user_id: uuid.UUID):
    try:
        user = await get_user_obj(user_id)
        user.is_active = False
        await user.update()
        return {"detail": f"l'utente {user.username} è stato disabilitato"}
    except NoMatch:
        raise HTTPException(status_code=404, detail="L'utente specificato non esiste nel database")


@router.post("/authorize_admin")
async def authorize_admin(user_id: uuid.UUID):
    try:
        user = await get_user_obj(user_id)
        user.is_active = True
        user.is_superuser = True
        await user.update()
        return {"detail": f"l'utente {user.username} ora è amministratore"}
    except NoMatch:
        raise HTTPException(status_code=404, detail="L'utente specificato non esiste nel database")


@router.post("/revoce_admin")
async def revoce_admin(user_id: uuid.UUID):
    try:
        user = await get_user_obj(user_id)
        user.is_active = True
        user.is_superuser = False
        await user.update()
        return {"detail": f"l'utente {user.username} non è più amministratore"}
    except NoMatch:
        raise HTTPException(status_code=404, detail="L'utente specificato non esiste nel database")


@router.post("/delete_user")
async def delete_user(user_id: uuid.UUID):
    try:
        user = await get_user_obj(user_id)
        await user.delete()
        return {"detail": f"l'utente {user.username} è stato eliminato"}
    except NoMatch:
        raise HTTPException(status_code=404, detail="L'utente specificato non esiste nel database")
