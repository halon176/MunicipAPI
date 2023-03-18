import ormar

from src.database import database, metadata


class Regioni(ormar.Model):
    class Meta:
        tablename = "regioni"
        metadata = metadata
        database = database
    id: int = ormar.Integer(primary_key=True)
    nome: str = ormar.String(max_length=100, unique=True)
    capoluogo: str = ormar.String(max_length=100)
    superficie: int = ormar.Integer()
    abitanti: int = ormar.Integer()


class Province(ormar.Model):
    class Meta:
        tablename = "province"
        metadata = metadata
        database = database
    id: int = ormar.Integer(primary_key=True)
    nome: str = ormar.String(max_length=100, unique=True)
    sigla: str =ormar.String(max_length=4)
    superficie: int = ormar.Integer()
    abitanti: int = ormar.Integer()
    regione: Regioni = ormar.ForeignKey(Regioni)



class Comuni(ormar.Model):
    class Meta:
        tablename = "comuni"
        metadata = metadata
        database = database
    id: int = ormar.Integer(primary_key=True)
    nome: str = ormar.String(max_length=100)
    istat: int = ormar.Integer()
    abitanti: int = ormar.Integer()
    CAP: int = ormar.Integer()
    codice_fiscale: str = ormar.String(max_length=5)
    prefisso: int = ormar.Integer()
    provincia: Province = ormar.ForeignKey(Province)

