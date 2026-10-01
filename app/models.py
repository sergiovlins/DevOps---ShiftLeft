"""
Modelo de dados da aplicação: representa uma Tarefa (Task) e um
repositório simples que guarda as tarefas em memória (um dicionário
Python). Não uso banco de dados de propósito, para manter o projeto
enxuto e fácil de rodar em qualquer ambiente da pipeline, sem
depender de serviços externos.
"""

from dataclasses import dataclass, asdict
from itertools import count


@dataclass
class Task:
    id: int
    titulo: str
    descricao: str = ""
    concluida: bool = False

    def to_dict(self):
        return asdict(self)


class TaskRepository:
    """
    Repositório em memória para as tarefas.

    Centralizo aqui toda a lógica de acesso aos dados (criar, buscar,
    atualizar, remover). Assim, se um dia eu quiser trocar o
    armazenamento em memória por um banco de dados de verdade, só
    preciso reescrever esta classe, sem mexer nas rotas.
    """

    def __init__(self):
        self._tasks = {}
        self._id_counter = count(1)

    def listar(self):
        return list(self._tasks.values())

    def buscar(self, task_id):
        return self._tasks.get(task_id)

    def criar(self, titulo, descricao=""):
        novo_id = next(self._id_counter)
        tarefa = Task(id=novo_id, titulo=titulo, descricao=descricao)
        self._tasks[novo_id] = tarefa
        return tarefa

    def atualizar(self, task_id, **campos):
        tarefa = self._tasks.get(task_id)
        if tarefa is None:
            return None
        for chave, valor in campos.items():
            if valor is not None and hasattr(tarefa, chave):
                setattr(tarefa, chave, valor)
        return tarefa

    def remover(self, task_id):
        return self._tasks.pop(task_id, None) is not None


# Instância única (singleton simples) usada pelas rotas da aplicação.
repositorio = TaskRepository()
