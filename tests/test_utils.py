"""
Testes da função de validação usada pelas rotas ao criar/atualizar
tarefas.
"""

from app.utils import validar_dados_tarefa


def test_dados_validos():
    valido, erro = validar_dados_tarefa({"titulo": "Tarefa ok"})
    assert valido is True
    assert erro is None


def test_titulo_obrigatorio_ausente():
    valido, erro = validar_dados_tarefa({"descricao": "sem titulo"})
    assert valido is False
    assert "titulo" in erro


def test_titulo_nao_obrigatorio_em_update():
    valido, _ = validar_dados_tarefa({"concluida": True}, exigir_titulo=False)
    assert valido is True


def test_titulo_tipo_invalido():
    valido, _ = validar_dados_tarefa({"titulo": 123})
    assert valido is False


def test_concluida_tipo_invalido():
    valido, _ = validar_dados_tarefa({"titulo": "ok", "concluida": "sim"})
    assert valido is False


def test_corpo_nulo():
    valido, _ = validar_dados_tarefa(None)
    assert valido is False
