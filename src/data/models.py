import ormar
from pydantic import BaseModel

from src.database import MainMeta, database, metadata

class Regioni(ormar.Model):
    class Meta(MainMeta):
        tablename = "regioni"

    id: int = ormar.Integer(primary_key=True)
    nome: str = ormar.String(max_length=100, unique=True)
    capoluogo: str = ormar.String(max_length=100)
    superficie: int = ormar.Integer()
    abitanti: int = ormar.Integer()


class Province(ormar.Model):
    class Meta(MainMeta):
        tablename = "province"

    id: int = ormar.Integer(primary_key=True)
    nome: str = ormar.String(max_length=100, unique=True)
    sigla: str =ormar.String(max_length=4)
    superficie: int = ormar.Integer()
    abitanti: int = ormar.Integer()
    regione: Regioni = ormar.ForeignKey(Regioni, related_name="province")

class Get_province(BaseModel):
    nome: str
    sigla: str
    superficie: int
    abitanti: int


class Comuni(ormar.Model):
    class Meta(MainMeta):
        tablename = "comuni"

    id: int = ormar.Integer(primary_key=True)
    nome: str = ormar.String(max_length=100)
    istat: int = ormar.Integer()
    abitanti: int = ormar.Integer()
    CAP: int = ormar.Integer()
    codice_fiscale: str = ormar.String(max_length=5)
    prefisso: int = ormar.Integer()
    provincia: Province = ormar.ForeignKey(Province, related_name="comuni")

class Get_comuni(BaseModel):
    nome: str
    CAP: int
    provincia: str

