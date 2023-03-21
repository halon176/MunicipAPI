from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

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


# Configurazione CORS per consentire le richieste dal tuo dominio React
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
    "http://192.168.1.30:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
