def _create(client, nome, notas):
    refeicao = client.post(
        "/refeicoes", json={"nome": nome, "tipo": "almoco", "data": "2026-11-26"}
    ).json()
    for nota in notas:
        client.post(f"/refeicoes/{refeicao['id']}/avaliacoes", json={"nota": nota})


def test_ranking_melhores(client):
    _create(client, "Feijoada", [5, 5])
    _create(client, "Lasanha", [2])
    _create(client, "Sopa sem nota", [])
    nomes = [r["nome"] for r in client.get("/ranking").json()]
    assert nomes == ["Feijoada", "Lasanha"]


def test_ranking_piores(client):
    _create(client, "Feijoada", [5])
    _create(client, "Lasanha", [1])
    nomes = [r["nome"] for r in client.get("/ranking?ordem=piores").json()]
    assert nomes == ["Lasanha", "Feijoada"]


def test_ranking_limite(client):
    for i in range(3):
        _create(client, f"Prato {i}", [i + 1])
    assert len(client.get("/ranking?limite=2").json()) == 2


def test_ranking_ordem_invalida(client):
    assert client.get("/ranking?ordem=meio").status_code == 422
