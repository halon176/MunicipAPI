from pydantic import BaseModel


class GetProvince(BaseModel):
    nome: str
    sigla: str
    superficie: int
    abitanti: int


class GetComuni(BaseModel):
    nome: str
    CAP: int
    provincia: str
    codice_fiscale: str
    prefisso: str


class GetRegioni(BaseModel):
    nome: str
    capoluogo: str
    superficie: int
    abitanti: int
