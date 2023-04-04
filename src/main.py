from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.auth.router_token import router as router_token
from src.config import REDIS_HOST
from src.data.router_comuni import router as router_comuni
from src.data.router_province import router as router_province
from src.data.router_regioni import router as router_regioni
from src.auth.router_user import router as router_user

from src.database import database
from redis import asyncio as aioredis

app = FastAPI(
    title="MunicipAPI",
    version="0.2.0",
    redoc_url=None
)

app.state.database = database
app.include_router(router_regioni)
app.include_router(router_comuni)
app.include_router(router_province)
app.include_router(router_token)
app.include_router(router_user)

@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()

@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url(f"redis://{REDIS_HOST}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


# CORS redirect to work with local react
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
    "http://192.168.1.30:3000"
    "http://192.168.43"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
