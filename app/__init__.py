"""
Pacote principal da aplicação.

Uso o padrão "application factory" (create_app) para poder
instanciar a aplicação Flask de formas diferentes: uma vez no
ambiente normal (run.py) e outra vez nos testes automatizados e no
scan dinâmico (DAST), sem que uma configuração interfira na outra.
"""

from pathlib import Path

from flask import Flask, send_from_directory

from app.routes import tasks_bp

# Pasta "images/" na raiz do projeto e a imagem exibida na página
# inicial. O nome do arquivo é fixo (e não vem da URL) para evitar
# qualquer risco de path traversal ao servir o arquivo.
PASTA_IMAGENS = Path(__file__).resolve().parent.parent / "images"
IMAGEM_INICIAL = "Aplicação em funcionamento.png"

PAGINA_INICIAL = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Aplicação em funcionamento</title>
  <style>
    html, body { margin: 0; height: 100%; background: #000; }
    body { display: flex; align-items: center; justify-content: center; }
    img { max-width: 100%; max-height: 100%; }
  </style>
</head>
<body>
  <img src="/imagem-inicial" alt="Aplicação em funcionamento">
</body>
</html>
"""


def create_app():
    app = Flask(__name__)

    # Registro o blueprint de tarefas, que concentra todas as rotas
    # relacionadas ao recurso "tasks" (/tasks, /tasks/<id>, etc).
    app.register_blueprint(tasks_bp)

    # Rota simples de verificação de saúde da aplicação (health check).
    # Uso essa rota tanto para monitoramento quanto para a pipeline
    # saber quando a aplicação já está pronta para receber o scan do
    # OWASP ZAP (etapa de DAST).
    @app.route("/health")
    def health():
        return {"status": "ok"}, 200

    # Página inicial: fundo preto com a imagem centralizada, só para
    # indicar visualmente que a aplicação está no ar.
    @app.route("/")
    def index():
        return PAGINA_INICIAL, 200, {"Content-Type": "text/html; charset=utf-8"}

    @app.route("/imagem-inicial")
    def imagem_inicial():
        return send_from_directory(PASTA_IMAGENS, IMAGEM_INICIAL)

    return app
