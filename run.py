"""Ponto de entrada da aplicação (uso local e na etapa de DAST da pipeline)."""

from app import create_app

app = create_app()

if __name__ == "__main__":
    # Falha proposital: host="0.0.0.0" é barrado pelo Semgrep (SAST) e
    # faz a pipeline falhar. Correção: host="127.0.0.1".
    app.run(host="0.0.0.0", port=5000, debug=False)
