import uuid

from fastapi import APIRouter, Depends, Request, HTTPException

from src.auth.models import JWTBearer, User, APIKey
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


@router.get("/user_list")
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
    except Exception:
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
    except Exception:
        raise HTTPException(status_code=404, detail="L'utente specificato non esiste nel database")


@router.post("/user_api_key")
async def user_api_key(user_id: uuid.UUID):
    user = await get_user_obj(user_id)
    user_apikey_list = await APIKey.objects.filter(user_id=user.id).all()
    return user_apikey_list


# per qualche motivo delete() continua a restituire None anche quando
# elimina un tot di righe
@router.post("/delete_all_user_apikey")
async def delete_all_user_apikey(user_id: uuid.UUID):
    user = await get_user_obj(user_id)
    await APIKey.objects.delete(user_id=user.id)
    return {"detail": f"Tutte le API-Key relative a {user.username} sono state eliminate"}
