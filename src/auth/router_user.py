import os
import secrets
from datetime import datetime
import ormar
import bcrypt
from datetime import datetime
import time
from typing import Dict



from fastapi import APIRouter, HTTPException, status, Depends
from email_validator import validate_email, EmailNotValidError

from src.auth.logic import signJWT
from src.auth.models import User, APIKey


router = APIRouter(
    prefix="/user",
    tags=["User"]
)




@router.get("/")
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
        if existing_token.id_user == user.id:
            return {"detail": "Login effettuato con successo, chiave esistente", "X-API-Key": existing_token.apikey}
    except ormar.exceptions.NoMatch:
        token = secrets.token_urlsafe(16)
        await APIKey.objects.create(apikey=token, user_id=user.id, created_at=datetime.now())
        return {"detail": "Login effettuato con successo", "X-API-Key": token}



# @router.post("/logout")
# async def remove_key(username: str):
#     user_to_remove = await User.objects.filter(username=username).first()
#     deleted_token = await APIKey.objects.delete(id_user=user_to_remove.id)
#     return f"la chiave {deleted_token}  dell'utente {user_to_remove.username} è stata eliminata"