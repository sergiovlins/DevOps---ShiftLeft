"""
Rotas HTTP do recurso "tasks".

Implemento uma API REST simples de gerenciamento de tarefas
(To-Do List), com as operações básicas de um CRUD:
  - Create: POST   /tasks
  - Read:   GET    /tasks e GET /tasks/<id>
  - Update: PUT    /tasks/<id>
  - Delete: DELETE /tasks/<id>

É essa API que será alvo tanto do SAST (análise do código abaixo)
quanto do DAST (ataque em tempo de execução feito pelo OWASP ZAP
contra esses mesmos endpoints já em funcionamento).
"""

from flask import Blueprint, jsonify, request

from app.models import repositorio
from app.utils import validar_dados_tarefa

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.get("")
def listar_tarefas():
    tarefas = [tarefa.to_dict() for tarefa in repositorio.listar()]
    return jsonify(tarefas), 200


@tasks_bp.get("/<int:task_id>")
def buscar_tarefa(task_id):
    tarefa = repositorio.buscar(task_id)
    if tarefa is None:
        return jsonify({"erro": "Tarefa não encontrada."}), 404
    return jsonify(tarefa.to_dict()), 200


@tasks_bp.post("")
def criar_tarefa():
    dados = request.get_json(silent=True)
    valido, erro = validar_dados_tarefa(dados)
    if not valido:
        return jsonify({"erro": erro}), 400

    tarefa = repositorio.criar(
        titulo=dados["titulo"],
        descricao=dados.get("descricao", ""),
    )
    return jsonify(tarefa.to_dict()), 201


@tasks_bp.put("/<int:task_id>")
def atualizar_tarefa(task_id):
    dados = request.get_json(silent=True)
    valido, erro = validar_dados_tarefa(dados, exigir_titulo=False)
    if not valido:
        return jsonify({"erro": erro}), 400

    tarefa = repositorio.atualizar(
        task_id,
        titulo=dados.get("titulo"),
        descricao=dados.get("descricao"),
        concluida=dados.get("concluida"),
    )
    if tarefa is None:
        return jsonify({"erro": "Tarefa não encontrada."}), 404
    return jsonify(tarefa.to_dict()), 200


@tasks_bp.delete("/<int:task_id>")
def remover_tarefa(task_id):
    removida = repositorio.remover(task_id)
    if not removida:
        return jsonify({"erro": "Tarefa não encontrada."}), 404
    return "", 204
