import uuid

from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.logic import JWTBearer
from src.auth.models import User, APIKey
from src.auth.router_token import get_uuid_bearer
from src.database import get_async_session

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(JWTBearer())]

)


async def get_user_obj(user_id: uuid.UUID, session: AsyncSession) -> User:
    query = select(User).where(User.id == user_id)
    user = (await session.scalars(query)).first()
    return user


async def verify_admin(request, session: AsyncSession):
    user_uuid = await get_uuid_bearer(request)
    query = select(User).where(User.id == user_uuid)
    user = (await session.scalars(query)).first()
    print(user.to_json())
    if user.is_superuser:
        return True
    else:
        return False


@router.get("/im_i_admin")
async def am_i_admin(request: Request, session: AsyncSession = Depends(get_async_session)):
    is_admin = await verify_admin(request, session)
    return is_admin


@router.get("/user_list")
async def user_list(session: AsyncSession = Depends(get_async_session)):
    query = select(User)
    users = (await session.scalars(query)).all()
    return users


@router.post("/activate_user")
async def activate_user(user_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(User).where(User.id == user_id)
        user = (await session.scalars(query)).first()
        user.is_active = True
        await session.commit()
        return {"detail": f"l'utente {user.username} è stato abilitato"}
    except Exception:
        raise HTTPException(status_code=404, detail="L'utente specificato non esiste nel database")


@router.post("/deactivate_user")
async def deactivate_user(user_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(User).where(User.id == user_id)
        user = (await session.scalars(query)).first()
        user.is_active = False
        await session.commit()
        return {"detail": f"l'utente {user.username} è stato disabilitato"}
    except Exception:
        raise HTTPException(status_code=404, detail="L'utente specificato non esiste nel database")



@router.post("/authorize_admin")
async def authorize_admin(user_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(User).where(User.id == user_id)
        user = (await session.scalars(query)).first()
        user.is_superuser = True
        await session.commit()
        return {"detail": f"l'utente {user.username} è ora amministratore"}
    except Exception:
        raise HTTPException(status_code=404, detail="L'utente specificato non esiste nel database")


@router.post("/revoce_admin")
async def revoce_admin(user_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(User).where(User.id == user_id)
        user = (await session.scalars(query)).first()
        user.is_superuser = False
        await session.commit()
        return {"detail": f"l'utente {user.username} non è più amministratore"}
    except Exception:
        raise HTTPException(status_code=404, detail="L'utente specificato non esiste nel database")


@router.post("/delete_user")
async def delete_user(user_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    try:
        query = delete(User).where(User.id == user_id)
        await session.execute(query)
        return {"detail": f"l'utente con id: {user_id} è stato eliminato"}
    except Exception:
        raise HTTPException(status_code=404, detail="L'utente specificato non esiste nel database")


@router.post("/user_api_key")
async def user_api_key(user_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    query = select(APIKey).where(APIKey.user_id == user_id)
    user_apikey = (await session.scalars(query)).all()
    return user_apikey


# per qualche motivo delete() continua a restituire None anche quando
# elimina un tot di righe
@router.post("/delete_all_user_apikey")
async def delete_all_user_apikey(user_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    user = await get_user_obj(user_id, session)
    query = delete(APIKey).where(APIKey.user_id == user.id)
    await session.execute(query)

    return {"detail": f"Tutte le API-Key relative a {user.username} sono state eliminate"}
