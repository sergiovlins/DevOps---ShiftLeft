"""
Testes de integração das rotas HTTP, usando o cliente de testes do
Flask.
"""

import pytest

from app import create_app
from app.models import repositorio


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    # Limpo o repositório em memória antes de cada teste, para que um
    # teste não interfira no resultado do outro.
    repositorio._tasks.clear()

    with app.test_client() as client:
        yield client


def test_health_check(client):
    resposta = client.get("/health")
    assert resposta.status_code == 200
    assert resposta.get_json() == {"status": "ok"}


def test_listar_tarefas_vazia(client):
    resposta = client.get("/tasks")
    assert resposta.status_code == 200
    assert resposta.get_json() == []


def test_criar_tarefa(client):
    resposta = client.post("/tasks", json={"titulo": "Estudar Shift Left"})
    assert resposta.status_code == 201
    corpo = resposta.get_json()
    assert corpo["titulo"] == "Estudar Shift Left"
    assert corpo["concluida"] is False


def test_criar_tarefa_sem_titulo(client):
    resposta = client.post("/tasks", json={"descricao": "faltou o titulo"})
    assert resposta.status_code == 400


def test_buscar_tarefa(client):
    criada = client.post("/tasks", json={"titulo": "Tarefa A"}).get_json()
    resposta = client.get(f"/tasks/{criada['id']}")
    assert resposta.status_code == 200
    assert resposta.get_json()["titulo"] == "Tarefa A"


def test_buscar_tarefa_inexistente(client):
    resposta = client.get("/tasks/999")
    assert resposta.status_code == 404


def test_atualizar_tarefa(client):
    criada = client.post("/tasks", json={"titulo": "Tarefa B"}).get_json()
    resposta = client.put(f"/tasks/{criada['id']}", json={"concluida": True})
    assert resposta.status_code == 200
    assert resposta.get_json()["concluida"] is True


def test_remover_tarefa(client):
    criada = client.post("/tasks", json={"titulo": "Tarefa C"}).get_json()
    resposta = client.delete(f"/tasks/{criada['id']}")
    assert resposta.status_code == 204

    resposta_get = client.get(f"/tasks/{criada['id']}")
    assert resposta_get.status_code == 404


def test_pagina_inicial(client):
    resposta = client.get("/")
    assert resposta.status_code == 200
    assert resposta.content_type.startswith("text/html")
    html = resposta.get_data(as_text=True)
    assert "background: #000" in html
    assert 'src="/imagem-inicial"' in html


def test_imagem_inicial(client):
    resposta = client.get("/imagem-inicial")
    assert resposta.status_code == 200
    assert resposta.content_type == "image/png"
    resposta.close()
