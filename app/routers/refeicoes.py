from typing import Literal

from fastapi import APIRouter, HTTPException, Response, status

from app.schemas import Avaliacao, AvaliacaoIn, Refeicao, RefeicaoIn
from app.storage import storage

router = APIRouter(prefix="/refeicoes", tags=["refeicoes"])

NOT_FOUND = "Refeicao nao encontrada"


@router.get("", response_model=list[Refeicao])
def list_refeicoes(
    tipo: Literal["almoco", "jantar"] | None = None, vegetariano: bool | None = None
) -> list[Refeicao]:
    return storage.list_refeicoes(tipo=tipo, vegetariano=vegetariano)


@router.get("/{refeicao_id}", response_model=Refeicao)
def get_refeicao(refeicao_id: int) -> Refeicao:
    refeicao = storage.get_refeicao(refeicao_id)
    if refeicao is None:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return refeicao


@router.post("", response_model=Refeicao, status_code=status.HTTP_201_CREATED)
def create_refeicao(data: RefeicaoIn) -> Refeicao:
    return storage.create_refeicao(data)


@router.delete("/{refeicao_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_refeicao(refeicao_id: int) -> Response:
    if not storage.delete_refeicao(refeicao_id):
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/{refeicao_id}/avaliacoes", response_model=Avaliacao, status_code=status.HTTP_201_CREATED
)
def create_avaliacao(refeicao_id: int, data: AvaliacaoIn) -> Avaliacao:
    avaliacao = storage.create_avaliacao(refeicao_id, data)
    if avaliacao is None:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return avaliacao


@router.get("/{refeicao_id}/avaliacoes", response_model=list[Avaliacao])
def list_avaliacoes(refeicao_id: int) -> list[Avaliacao]:
    if storage.get_refeicao(refeicao_id) is None:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return storage.list_avaliacoes(refeicao_id)
