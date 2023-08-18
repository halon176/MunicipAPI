from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Regione(Base):
    __tablename__ = "regioni"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), unique=True)
    capoluogo: Mapped[str] = mapped_column(String(100))
    superficie: Mapped[int] = mapped_column(Integer)
    abitanti: Mapped[int] = mapped_column(Integer)


class Provincia(Base):
    __tablename__ = "province"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), unique=True)
    sigla: Mapped[str] = mapped_column(String(4))
    superficie: Mapped[int] = mapped_column(Integer)
    abitanti: Mapped[int] = mapped_column(Integer)
    regione_id: Mapped[int] = mapped_column(Integer)


class Comune(Base):
    __tablename__ = "comuni"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), unique=True)
    istat: Mapped[int] = mapped_column(Integer)
    abitanti: Mapped[int] = mapped_column(Integer)
    CAP: Mapped[int] = mapped_column(Integer)
    codice_fiscale: Mapped[str] = mapped_column(String(6), unique=True)
    prefisso: Mapped[int] = mapped_column()
