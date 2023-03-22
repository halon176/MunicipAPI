import os
import secrets
from datetime import datetime
import ormar

import bcrypt
from email_validator import validate_email, EmailNotValidError
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import APIKeyHeader

from src.auth.models import User, APIKey

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.get("/")
async def user_list():
    userlist = await User.objects.all()
    return userlist


X_API_KEY = APIKeyHeader(name='X-API-Key')


async def api_key_auth(x_api_key: str = Depends(X_API_KEY)):
    apikey = await APIKey.objects.filter(apikey=x_api_key).get()
    os.environ['API-KEY'] = apikey.apikey
    if x_api_key != os.environ['API-KEY']:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key. Check that you are passing a 'X-API-Key' on your header."
        )


async def api_key_auth_admin(x_api_key: str = Depends(X_API_KEY)):
    apikey = await APIKey.objects.filter(apikey=x_api_key).get()
    os.environ['API-KEY'] = apikey.apikey
    if x_api_key != os.environ['API-KEY']:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key. Check that you are passing a 'X-API-Key' on your header."
        )


@router.post("/add_user")
async def create_user(username, email, password):
    try:
        valid_email = validate_email(email)
        email = valid_email.email
    except EmailNotValidError as e:
        return f"L'email inserita non è valida: {e}"

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    await User.objects.create(username=username, email=email, hashed_password=hashed_password)
    return f"Utente {username} è stato creato"


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
        existing_token = await APIKey.objects.filter(id_user=user.id).first()
        if existing_token.id_user == user.id:
            return {"detail": "Login effettuato con successo, chiave esistente", "X-API-Key": existing_token.apikey}
    except ormar.exceptions.NoMatch:
        token = secrets.token_urlsafe(16)
        await APIKey.objects.create(apikey=token, id_user=user.id, created_at=datetime.now())
        return {"detail": "Login effettuato con successo", "X-API-Key": token}



@router.post("/logout")
async def remove_key(username: str):
    user_to_remove = await User.objects.filter(username=username).first()
    deleted_token = await APIKey.objects.delete(id_user=user_to_remove.id)
    return f"la chiave {deleted_token}  dell'utente {user_to_remove.username} è stata eliminata"