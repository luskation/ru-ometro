import pytest


def test_create_avaliacao(client, refeicao):
    url = f"/refeicoes/{refeicao['id']}/avaliacoes"
    response = client.post(url, json={"nota": 4, "comentario": "Bom!"})
    assert response.status_code == 201
    body = response.json()
    assert body["nota"] == 4
    assert body["refeicao_id"] == refeicao["id"]
    assert "criado_em" in body


@pytest.mark.parametrize("nota", [0, 6, -1])
def test_create_avaliacao_invalid_nota(client, refeicao, nota):
    url = f"/refeicoes/{refeicao['id']}/avaliacoes"
    assert client.post(url, json={"nota": nota}).status_code == 422


def test_create_avaliacao_refeicao_not_found(client):
    assert client.post("/refeicoes/999/avaliacoes", json={"nota": 3}).status_code == 404


def test_media_and_total(client, refeicao):
    url = f"/refeicoes/{refeicao['id']}/avaliacoes"
    for nota in [5, 4, 3]:
        client.post(url, json={"nota": nota})
    body = client.get(f"/refeicoes/{refeicao['id']}").json()
    assert body["media"] == 4.0
    assert body["total_avaliacoes"] == 3
    assert len(client.get(url).json()) == 3
