import bcrypt
from email_validator import validate_email, EmailNotValidError
from fastapi import APIRouter, HTTPException, status

from src.auth.logic import signJWT
from src.auth.models import User

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


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
    try:
        user = await User.objects.filter(username=username).first()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenziali errate")

    if not user.check_password(password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenziali errate")

    if not user.check_active():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Utente non ancora autorizzato")

    return signJWT(user.id)
