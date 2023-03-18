from typing import List

from fastapi import FastAPI

from src.database import database

from src.data.router_regioni import router as router_regioni
from src.data.router_comuni import router as router_comuni


app = FastAPI(
    title="MunicipAPI"
)

app.state.database = database
app.include_router(router_regioni)
app.include_router(router_comuni)


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
