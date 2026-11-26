"""In-memory repository. Data is lost on restart (by design: no database)."""

import threading
from datetime import UTC, date, datetime

from app.schemas import Avaliacao, AvaliacaoIn, Refeicao, RefeicaoIn


class Storage:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self.reset()

    def reset(self) -> None:
        with self._lock:
            self._refeicoes: dict[int, RefeicaoIn] = {}
            self._avaliacoes: dict[int, Avaliacao] = {}
            self._next_refeicao_id = 1
            self._next_avaliacao_id = 1

    def _to_refeicao(self, refeicao_id: int, data: RefeicaoIn) -> Refeicao:
        notas = [a.nota for a in self._avaliacoes.values() if a.refeicao_id == refeicao_id]
        media = round(sum(notas) / len(notas), 2) if notas else None
        return Refeicao(
            id=refeicao_id, media=media, total_avaliacoes=len(notas), **data.model_dump()
        )

    def list_refeicoes(
        self, tipo: str | None = None, vegetariano: bool | None = None
    ) -> list[Refeicao]:
        with self._lock:
            result = [self._to_refeicao(i, r) for i, r in self._refeicoes.items()]
        if tipo is not None:
            result = [r for r in result if r.tipo == tipo]
        if vegetariano is not None:
            result = [r for r in result if r.vegetariano == vegetariano]
        return result

    def get_refeicao(self, refeicao_id: int) -> Refeicao | None:
        with self._lock:
            data = self._refeicoes.get(refeicao_id)
            return self._to_refeicao(refeicao_id, data) if data else None

    def create_refeicao(self, data: RefeicaoIn) -> Refeicao:
        with self._lock:
            refeicao_id = self._next_refeicao_id
            self._next_refeicao_id += 1
            self._refeicoes[refeicao_id] = data
            return self._to_refeicao(refeicao_id, data)

    def delete_refeicao(self, refeicao_id: int) -> bool:
        with self._lock:
            if refeicao_id not in self._refeicoes:
                return False
            del self._refeicoes[refeicao_id]
            self._avaliacoes = {
                k: a for k, a in self._avaliacoes.items() if a.refeicao_id != refeicao_id
            }
            return True

    def create_avaliacao(self, refeicao_id: int, data: AvaliacaoIn) -> Avaliacao | None:
        with self._lock:
            if refeicao_id not in self._refeicoes:
                return None
            avaliacao = Avaliacao(
                id=self._next_avaliacao_id,
                refeicao_id=refeicao_id,
                criado_em=datetime.now(UTC),
                **data.model_dump(),
            )
            self._next_avaliacao_id += 1
            self._avaliacoes[avaliacao.id] = avaliacao
            return avaliacao

    def list_avaliacoes(self, refeicao_id: int) -> list[Avaliacao]:
        with self._lock:
            return [a for a in self._avaliacoes.values() if a.refeicao_id == refeicao_id]

    def seed(self) -> None:
        hoje = date.today()
        exemplos = [
            (RefeicaoIn(nome="Feijoada", tipo="almoco", data=hoje), [5, 4, 5]),
            (RefeicaoIn(nome="Strogonoff de frango", tipo="jantar", data=hoje), [4, 3]),
            (
                RefeicaoIn(
                    nome="Lasanha de berinjela", tipo="almoco", data=hoje, vegetariano=True
                ),
                [3, 2, 4],
            ),
            (RefeicaoIn(nome="Sopa de legumes", tipo="jantar", data=hoje, vegetariano=True), []),
        ]
        for refeicao, notas in exemplos:
            criada = self.create_refeicao(refeicao)
            for nota in notas:
                self.create_avaliacao(criada.id, AvaliacaoIn(nota=nota))


storage = Storage()
