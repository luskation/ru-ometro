def test_create_refeicao(client):
    payload = {"nome": "Feijoada", "tipo": "almoco", "data": "2026-11-26"}
    response = client.post("/refeicoes", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["vegetariano"] is False
    assert body["media"] is None
    assert body["total_avaliacoes"] == 0


def test_create_refeicao_invalid_tipo(client):
    payload = {"nome": "Feijoada", "tipo": "cafe", "data": "2026-11-26"}
    assert client.post("/refeicoes", json=payload).status_code == 422


def test_create_refeicao_nome_too_short(client):
    payload = {"nome": "ab", "tipo": "almoco", "data": "2026-11-26"}
    assert client.post("/refeicoes", json=payload).status_code == 422


def test_get_refeicao(client, refeicao):
    response = client.get(f"/refeicoes/{refeicao['id']}")
    assert response.status_code == 200
    assert response.json()["nome"] == "Feijoada"


def test_get_refeicao_not_found(client):
    response = client.get("/refeicoes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Refeicao nao encontrada"


def test_list_refeicoes_filters(client):
    client.post("/refeicoes", json={"nome": "Feijoada", "tipo": "almoco", "data": "2026-11-26"})
    client.post(
        "/refeicoes",
        json={"nome": "Sopa", "tipo": "jantar", "data": "2026-11-26", "vegetariano": True},
    )
    assert len(client.get("/refeicoes").json()) == 2
    assert [r["nome"] for r in client.get("/refeicoes?tipo=almoco").json()] == ["Feijoada"]
    assert [r["nome"] for r in client.get("/refeicoes?vegetariano=true").json()] == ["Sopa"]


def test_delete_refeicao(client, refeicao):
    client.post(f"/refeicoes/{refeicao['id']}/avaliacoes", json={"nota": 5})
    assert client.delete(f"/refeicoes/{refeicao['id']}").status_code == 204
    assert client.get(f"/refeicoes/{refeicao['id']}").status_code == 404
    assert client.get(f"/refeicoes/{refeicao['id']}/avaliacoes").status_code == 404


def test_delete_refeicao_not_found(client):
    assert client.delete("/refeicoes/999").status_code == 404
