from typing import List

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Regione(Base):
    __tablename__ = "regioni"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), unique=True)
    capoluogo: Mapped[str] = mapped_column(String(100))
    superficie: Mapped[int] = mapped_column(Integer)
    abitanti: Mapped[int] = mapped_column(Integer)

    province: Mapped[List["Provincia"]] = relationship(back_populates="regione")


class Provincia(Base):
    __tablename__ = "province"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), unique=True)
    sigla: Mapped[str] = mapped_column(String(4))
    superficie: Mapped[int] = mapped_column(Integer)
    abitanti: Mapped[int] = mapped_column(Integer)
    regione_id: Mapped[int] = mapped_column(Integer, ForeignKey("regioni.id"))

    regione = relationship("Regione", back_populates="province")
    comune: Mapped[List["Comune"]] = relationship(back_populates="provincia")


class Comune(Base):
    __tablename__ = "comuni"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    istat: Mapped[int] = mapped_column(Integer)
    abitanti: Mapped[int] = mapped_column(Integer)
    CAP: Mapped[int] = mapped_column(Integer)
    codice_fiscale: Mapped[str] = mapped_column(String(6), unique=True)
    prefisso: Mapped[int] = mapped_column()
    provincia_id: Mapped[int] = mapped_column(Integer, ForeignKey("province.id"))

    provincia: Mapped["Provincia"] = relationship(back_populates="comune", lazy="joined")

    def to_json(self):
        return {
            "nome": self.nome,
            "CAP": self.CAP,
            "istat": self.istat,
            "abitanti": self.abitanti,
            "codice_fiscale": self.codice_fiscale,
            "prefisso": self.prefisso,
            "provincia": self.provincia.nome
        }
