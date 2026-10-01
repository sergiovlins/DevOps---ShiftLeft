"""
Funções utilitárias de validação, separadas das rotas para que
possam ser testadas isoladamente e reaproveitadas em outros pontos
da aplicação, se necessário.
"""


def validar_dados_tarefa(dados, exigir_titulo=True):
    """
    Valida o corpo (JSON) recebido para criar ou atualizar uma tarefa.

    Retorna uma tupla (valido, mensagem_erro). Se "valido" for False,
    a rota deve responder com HTTP 400 e a mensagem de erro.
    """
    if dados is None:
        return False, "Corpo da requisição precisa ser um JSON válido."

    titulo = dados.get("titulo")
    if exigir_titulo and not titulo:
        return False, "O campo 'titulo' é obrigatório."

    if titulo is not None and not isinstance(titulo, str):
        return False, "O campo 'titulo' deve ser uma string."

    descricao = dados.get("descricao")
    if descricao is not None and not isinstance(descricao, str):
        return False, "O campo 'descricao' deve ser uma string."

    concluida = dados.get("concluida")
    if concluida is not None and not isinstance(concluida, bool):
        return False, "O campo 'concluida' deve ser um booleano."

    return True, None
