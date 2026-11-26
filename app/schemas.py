from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field


class RefeicaoIn(BaseModel):
    nome: str = Field(min_length=3, max_length=100)
    tipo: Literal["almoco", "jantar"]
    data: date
    vegetariano: bool = False
    descricao: str | None = Field(default=None, max_length=280)


class Refeicao(RefeicaoIn):
    id: int
    media: float | None = None
    total_avaliacoes: int = 0


class AvaliacaoIn(BaseModel):
    nota: int = Field(ge=1, le=5)
    comentario: str | None = Field(default=None, max_length=280)


class Avaliacao(AvaliacaoIn):
    id: int
    refeicao_id: int
    criado_em: datetime


class Health(BaseModel):
    status: str
    version: str
