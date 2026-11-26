from typing import Literal

from fastapi import APIRouter, Query

from app.schemas import Refeicao
from app.storage import storage

router = APIRouter(tags=["ranking"])


@router.get("/ranking", response_model=list[Refeicao])
def ranking(
    ordem: Literal["melhores", "piores"] = "melhores",
    limite: int = Query(default=5, ge=1, le=100),
) -> list[Refeicao]:
    avaliadas = [r for r in storage.list_refeicoes() if r.media is not None]
    avaliadas.sort(key=lambda r: r.media, reverse=(ordem == "melhores"))
    return avaliadas[:limite]
