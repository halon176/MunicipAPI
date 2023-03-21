import ormar
from pydantic import BaseModel
from src.database import metadata, database


class Regioni(ormar.Model):
    class Meta:
        metadata = metadata
        database = database
        tablename = "regioni"

    id: int = ormar.Integer(primary_key=True)
    nome: str = ormar.String(max_length=100, unique=True)
    capoluogo: str = ormar.String(max_length=100)
    superficie: int = ormar.Integer()
    abitanti: int = ormar.Integer()


class Province(ormar.Model):
    class Meta:
        metadata = metadata
        database = database
        tablename = "province"

    id: int = ormar.Integer(primary_key=True)
    nome: str = ormar.String(max_length=100, unique=True)
    sigla: str = ormar.String(max_length=4)
    superficie: int = ormar.Integer()
    abitanti: int = ormar.Integer()
    regione: Regioni = ormar.ForeignKey(Regioni, related_name="province")


class GetProvince(BaseModel):
    nome: str
    sigla: str
    superficie: int
    abitanti: int


class Comuni(ormar.Model):
    class Meta:
        metadata = metadata
        database = database
        tablename = "comuni"

    id: int = ormar.Integer(primary_key=True)
    nome: str = ormar.String(max_length=100)
    istat: int = ormar.Integer()
    abitanti: int = ormar.Integer()
    CAP: int = ormar.Integer()
    codice_fiscale: str = ormar.String(max_length=5)
    prefisso: int = ormar.Integer()
    provincia: Province = ormar.ForeignKey(Province, related_name="comuni")


class GetComuni(BaseModel):
    nome: str
    CAP: int
    provincia: str

class GetRegioni(BaseModel):
    nome: str
    capoluogo: str
    superficie: int
    abitanti: int