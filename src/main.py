from fastapi import FastAPI, Depends

from src.auth.router_user import router as router_user, api_key_auth
from src.data.router_comuni import router as router_comuni
from src.data.router_province import router as router_province
from src.data.router_regioni import router as router_regioni
from src.database import database

app = FastAPI(
    title="MunicipAPI"
)

app.state.database = database
app.include_router(router_regioni)
app.include_router(router_comuni)
app.include_router(router_province)
app.include_router(router_user)


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


@app.get("/do_something", dependencies=[Depends(api_key_auth)])
async def do_something():
    return "API is working OK."
