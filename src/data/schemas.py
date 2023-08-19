from pydantic import BaseModel, Field


class ProvinciaResponse(BaseModel):
    nome: str = Field(..., examples=["Roma"])
    sigla: str = Field(..., examples=["RM"])
    superficie: int = Field(..., examples=[100])
    abitanti: int = Field(..., examples=[1000000])


class ComuneResponse(BaseModel):
    nome: str = Field(..., examples=["Roma"])
    CAP: int = Field(..., examples=[10])
    provincia: str = Field(..., examples=["Roma"])
    codice_fiscale: str = Field(..., examples=["H501"])
    prefisso: int = Field(..., examples=[39])


class RegioneResponse(BaseModel):
    nome: str = Field(..., examples=["Lazio"])
    capoluogo: str = Field(..., examples=["Roma"])
    superficie: int = Field(..., examples=[100])
    abitanti: int = Field(..., examples=[1000000])
