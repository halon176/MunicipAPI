import os

from fastapi import APIRouter, Depends, Request
from fastapi.security import APIKeyHeader

from src.auth.models import APIKey
from src.auth.router_token import read_host

router = APIRouter(
    prefix="/verify",
    tags=["Verify"],
)

X_API_KEY = APIKeyHeader(name='X-API-Key')


@router.get("/")
async def verify_apikey(request: Request, x_api_key: str = Depends(X_API_KEY)):
    try:
        apikey = await APIKey.objects.filter(apikey=x_api_key).get()
        os.environ['API-KEY'] = apikey.apikey
        if apikey.ip is not None and apikey.ip != read_host(request):
            return False
        else:
            return True
    except Exception:
        return False
