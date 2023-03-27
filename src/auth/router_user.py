import secrets
from datetime import datetime

import bcrypt
import ormar
from email_validator import validate_email, EmailNotValidError
from fastapi import APIRouter, HTTPException, status, Depends

from src.auth.logic import signJWT
from src.auth.models import User, APIKey
from src.auth.router_token import api_key_auth

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.get("/", dependencies=[Depends(api_key_auth)])
async def user_list():
    userlist = await User.objects.all()
    return userlist


@router.post("/add_user")
async def create_user(username, email, password):
    try:
        valid_email = validate_email(email)
        email = valid_email.email
    except EmailNotValidError as e:
        return f"L'email inserita non è valida: {e}"

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user = await User.objects.create(username=username, email=email, hashed_password=hashed_password)
    return signJWT(str(user.id))


@router.post("/login")
async def user_login(username: str, password: str):
    user = await User.objects.filter(username=username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_FORBIDDEN, detail="Credenziali errate")
    if not user.check_password(password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenziali errate")
    if not user.check_active():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Utente non ancora autorizzato")
    try:
        existing_token = await APIKey.objects.filter(user_id=user.id).first()
        if existing_token.user_id == user.id:
            return {"detail": "Login effettuato con successo, chiave esistente",
                    "X-API-Key": existing_token.apikey,
                    "Bearer Token": signJWT(user.id)}
    except ormar.exceptions.NoMatch:
        token = secrets.token_urlsafe(16)
        await APIKey.objects.create(apikey=token, user_id=user.id, created_at=datetime.now())
        return {"detail": "Login effettuato con successo",
                "X-API-Key": token,
                "Bearer Token": signJWT(user.id)}
