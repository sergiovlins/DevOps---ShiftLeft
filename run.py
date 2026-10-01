"""
Ponto de entrada da aplicação. É este arquivo que sobe o servidor de
desenvolvimento do Flask quando executo o projeto localmente, e
também o que a pipeline executa em segundo plano antes de rodar o
OWASP ZAP (etapa de DAST), já que o ZAP precisa de uma aplicação de
verdade no ar para poder atacá-la.
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
