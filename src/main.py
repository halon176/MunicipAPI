from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from src.auth.router_admin import router as router_admin
from src.auth.router_token import router as router_token
from src.auth.router_user import router as router_user
from src.auth.router_verify import router as router_verify
from src.config import REDIS_HOST
from src.data.router_comuni import router as router_comuni
from src.data.router_province import router as router_province
from src.data.router_regioni import router as router_regioni

app = FastAPI(
    title="MunicipAPI",
    version="0.2.0",
    # root_path="/api.municipapi",
    redoc_url=None,
    default_response_class=ORJSONResponse
)

app.include_router(router_regioni)
app.include_router(router_comuni)
app.include_router(router_province)
app.include_router(router_token)
app.include_router(router_user)
app.include_router(router_admin)
app.include_router(router_verify)


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url(f"redis://{REDIS_HOST}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
