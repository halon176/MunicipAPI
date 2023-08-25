import bcrypt
from email_validator import validate_email, EmailNotValidError
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.logic import signJWT
from src.auth.models import User
from src.database import get_async_session

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.post("/add_user")
async def create_user(username, email, password, session: AsyncSession = Depends(get_async_session)):
    try:
        valid_email = validate_email(email)
        email = valid_email.email
    except EmailNotValidError as e:
        return f"L'email inserita non è valida: {e}"

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = User(username=username, email=email, hashed_password=hashed_password)
    print(new_user.id)

    session.add(new_user)
    try:
        await session.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Errore durante l'inserimento dell'utente: {e}")
    return signJWT(new_user.id)


@router.post("/login")
async def user_login(username: str, password: str, session: AsyncSession = Depends(get_async_session)):
    query = select(User).where(User.username == username)
    user = (await session.scalars(query)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenziali errate")
    if not user.check_password(password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenziali errate")
    if not user.check_active():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Utente non ancora autorizzato")

    return signJWT(user.id)
