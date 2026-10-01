"""
Testes unitários do TaskRepository, isolados da camada HTTP.
"""

from app.models import TaskRepository


def test_criar_tarefa():
    repo = TaskRepository()
    tarefa = repo.criar("Estudar DevSecOps", "Ler sobre Shift Left")
    assert tarefa.id == 1
    assert tarefa.titulo == "Estudar DevSecOps"
    assert tarefa.concluida is False


def test_listar_tarefas():
    repo = TaskRepository()
    repo.criar("Tarefa 1")
    repo.criar("Tarefa 2")
    assert len(repo.listar()) == 2


def test_buscar_tarefa_existente():
    repo = TaskRepository()
    criada = repo.criar("Tarefa X")
    encontrada = repo.buscar(criada.id)
    assert encontrada is criada


def test_buscar_tarefa_inexistente():
    repo = TaskRepository()
    assert repo.buscar(999) is None


def test_atualizar_tarefa():
    repo = TaskRepository()
    tarefa = repo.criar("Tarefa original")
    atualizada = repo.atualizar(tarefa.id, titulo="Tarefa editada", concluida=True)
    assert atualizada.titulo == "Tarefa editada"
    assert atualizada.concluida is True


def test_atualizar_tarefa_inexistente():
    repo = TaskRepository()
    assert repo.atualizar(999, titulo="Não existe") is None


def test_remover_tarefa():
    repo = TaskRepository()
    tarefa = repo.criar("Tarefa a remover")
    assert repo.remover(tarefa.id) is True
    assert repo.buscar(tarefa.id) is None


def test_remover_tarefa_inexistente():
    repo = TaskRepository()
    assert repo.remover(999) is False
