# Projeto de Scan Automático - Aplicação de Shift-Left

Pipeline de **DevSecOps / Shift Left** aplicada a uma pequena API REST em Flask, integrando análise de segurança automatizada (SAST, SCA e DAST) ao processo de desenvolvimento via **GitHub Actions**, com a infraestrutura final descrita como código usando **Terraform**.

## 1. Sobre o projeto

O projeto é composto por duas partes:

* **Aplicação (`app/`)**: Uma API REST simples em Flask para gerenciar tarefas CRUD, acompanhada de testes automatizados (`tests/`). Ela serve como alvo real das análises de segurança.

* **Pipeline de Segurança (`.github/workflows/security.yml`)**: O foco principal da atividade. A cada `push` ou `pull request` na branch `main`, a pipeline executa automaticamente os testes automatizados, análise estática do código (**SAST**), análise das dependências (**SCA**), análise dinâmica da aplicação em execução (**DAST**) e a validação/geração da infraestrutura em código com **Terraform**.

## *A aplicação foi reutilizada de uma prática anterior no GitLab e adaptada para este ecossistema, utilizando o GitHub Actions como ferramenta principal de CI/CD*

A ideia central é aplicar o conceito de **Shift Left**: em vez de tratar a segurança apenas na fase final de desenvolvimento ou em produção, cada alteração de código passa por verificações de segurança automáticas desde o início do ciclo de desenvolvimento, prevenindo a introdução de falhas conhecidas e vulnerabilidades no repositório principal.
---

## 2. Ferramentas utilizadas

| Ferramenta  | Tipo de análise | Por que essa ferramenta? |
|-------------|------------------|---------------------------|
| **Semgrep** | SAST | É open-source, não exige servidor próprio (diferente do SonarQube, que precisa de uma instância rodando), tem regras prontas e atualizadas para Python/Flask (`--config auto`) e roda em segundos direto na pipeline via sua própria imagem Docker oficial. |
| **pip-audit** | SCA | É mantido pela própria Python Packaging Authority (PyPA), é feito especificamente para o ecossistema Python (lê `requirements.txt` nativamente) e consulta a base pública de vulnerabilidades do Python (PyPI Advisory Database), sem precisar de conta, chave de API ou serviço externo pago. |
| **OWASP ZAP** (baseline scan) | DAST | É o padrão de mercado para DAST open-source, mantido pela própria OWASP, e possui uma GitHub Action oficial (`zaproxy/action-baseline`) que facilita a integração direta na pipeline, sem precisar hospedar a ferramenta em outro lugar. |
| **Terraform** | IaC | Permite descrever o estado final da infraestrutura (configuração de ambiente + proxy reverso endurecido) de forma declarativa e versionada, sem a necessidade de subir uma imagem Docker ou depender de um provedor de nuvem pago para esta atividade (uso o provider `local`). |
| **Trivy** (bônus, dentro do job `terraform`) | SAST para IaC | Complementa o Terraform aplicando segurança também sobre o *código de infraestrutura* em si (ex.: evitar más práticas no próprio `.tf`), e não só sobre a aplicação. |

> Docker não foi utilizado nesta entrega, 
> sendo o Terraform que irá descrever o estado
> final do ambiente sem a necessidade de build/execução de uma
> imagem Docker.
> As escolhas das ferramentas foram realizadas com base na experiência que já tive em sala de aula, e as que considerei menos complexas para a execução completa do projeto. 

---

## 3. Tipo de análise

| Ferramenta | Sigla | O que verifica |
|------------|-------|-----------------|
| Semgrep    | SAST  | Código-fonte da aplicação (`app/`), sem executá-la |
| pip-audit  | SCA   | Dependências de terceiros listadas em `requirements.txt` |
| OWASP ZAP  | DAST  | A aplicação **em execução**, atacada via HTTP como um usuário externo faria |

---

## 4. Funcionamento da pipeline

**O que dispara a pipeline?**
Qualquer `push` ou `pull request` direcionado à branch `main`
(configurado em `on:` no início do `security.yml`).

**Em qual etapa ocorre a análise?**
A pipeline é dividida em jobs sequenciais (cada um só roda se o
anterior passar), seguindo o fluxo pedido:
```
Push / Pull Request
        │
        ▼
     [ test ]        → pytest (garante que a aplicação funciona)
        │
        ▼
     [ sast ]         → Semgrep analisa o código-fonte
        │
        ▼
     [ sca  ]         → pip-audit analisa as dependências
        │
        ▼
     [ dast ]         → aplicação sobe em background e o OWASP ZAP
                         faz o scan dinâmico contra ela
        │
        ▼
   [ terraform ]      → valida, escaneia (Trivy) e aplica a
                         infraestrutura como código
        │
        ▼
   [ resultado ]      → PASS (só roda se tudo acima passou)
```

**O que acontece quando são encontrados problemas?**
Cada job de segurança (`sast`, `sca`, `dast`, `terraform`) tem um
"portão de qualidade": se a ferramenta encontrar um problema (finding
do Semgrep, CVE do pip-audit, alerta do ZAP ou má prática do Trivy),
o respectivo passo retorna um código de saída diferente de zero, o
job falha, os jobs seguintes são automaticamente cancelados pelo
GitHub Actions, e a pipeline inteira fica marcada como **vermelha
(FAIL)** na aba "Actions" do repositório. O job `resultado` só
executa (e mostra PASS) quando absolutamente tudo passou.

Antes de cada portão de qualidade, a pipeline também gera um
relatório da ferramenta em formato JSON e salva como **artefato** do
GitHub Actions (`actions/upload-artifact`), para que o resultado
completo da análise fique disponível para download mesmo quando a
pipeline falha.

---

## 5. Resultados

### 5.1 Execução da pipeline

<img width="876" height="597" alt="Evidências 1" src="https://github.com/user-attachments/assets/d94b486f-a3e1-4c89-9edb-f5882186b8fd" />

### 5.2 Resultado do Semgrep (SAST)

<img width="1194" height="642" alt="Evidências 3" src="https://github.com/user-attachments/assets/261d72b8-e9a5-42c8-8f73-3f0a886dee6d" />

<img width="1285" height="446" alt="Captura de tela de 2026-10-01 18-10-54" src="https://github.com/user-attachments/assets/657d2da8-4914-45e8-9471-7270140a064f" />

### 5.3 Resultado do pip-audit (SCA)

<img width="880" height="145" alt="Evidências 4" src="https://github.com/user-attachments/assets/bba82d28-ee08-4550-a246-0e4c93316dd4" />


### 5.4 Resultado do OWASP ZAP (DAST)

<img width="1300" height="654" alt="Captura de tela de 2026-10-01 18-15-38" src="https://github.com/user-attachments/assets/56058f3c-d9d8-4832-b08e-910b347988a3" />

<img width="1290" height="694" alt="Captura de tela de 2026-10-01 18-15-23" src="https://github.com/user-attachments/assets/96cd82e8-0aa1-4dd6-96b4-507f123a0682" />

### 5.5 Resultado do GitHub Actions

> **Falha esperada na pipeline:** o job **SAST - Semgrep** falha por causa
> de um achado bloqueante em `run.py` (linha 10): `app.run(host="0.0.0.0", ...)`.
> Esse parâmetro expõe o servidor Flask em todas as interfaces de rede, e o
> Semgrep o identifica pela regra
> `python.flask.security.audit.app-run-param-config.avoid_app_run_with_bad_host`.
> Como o passo `semgrep scan --config auto --error` encerra com erro, a
> pipeline fica vermelha no GitHub Actions. Esse é o Shift Left funcionando:
> a falha de segurança é barrada na pipeline antes de chegar à produção.
> A correção é trocar o host para `127.0.0.1`.

<!-- Print da execução da pipeline com a falha do Semgrep -->

<img width="927" height="359" alt="Captura de tela de 2026-10-01 18-50-55" src="https://github.com/user-attachments/assets/659cab92-d030-4241-a39b-9df46a52667f" />


## 6. Como executar o projeto localmente

Abaixo está o passo a passo para instalar todas as dependências e
rodar a aplicação e as três ferramentas de segurança localmente, para
Linux e Windows.

### 6.1 Pré-requisitos

- Python 3.12+
- Git
- Terraform 1.6+ (apenas se for rodar a parte de infraestrutura)
- Java 11+ (necessário apenas se optar por rodar o OWASP ZAP via
  instalação nativa, em vez de Docker)

### 6.2 Linux

```bash
# 1. Clonar o repositório
git clone https://github.com/sergiovlins/DevOps---ShiftLeft.git
cd devsecops-scan

# 2. Criar e ativar um ambiente virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instalar as dependências da aplicação
pip install -r requirements.txt

# 4. Rodar os testes automatizados
pytest -v --cov=app

# 5. Subir a aplicação localmente
python run.py
# A API fica disponível em http://localhost:5000
# (teste em outro terminal: curl http://localhost:5000/health
```

**Instalando e rodando o Semgrep (SAST):**

```bash
pip install semgrep
semgrep scan --config auto
```

**Instalando e rodando o pip-audit (SCA):**

```bash
pip install pip-audit
pip-audit -r requirements.txt
```

**Rodando o OWASP ZAP (DAST) via Docker (forma mais simples no Linux):**

```bash
# com a aplicação já rodando em outro terminal (python run.py)
docker run -t --network="host" ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py -t http://localhost:5000
```

Se preferir não usar Docker, é possível baixar o OWASP ZAP Desktop
(https://www.zaproxy.org/download/) e rodar o scan "Automated Scan"
pela interface gráfica, apontando para `http://localhost:5000`.

**Rodando o Terraform:**

```bash
cd terraform
terraform init
terraform validate
terraform plan
terraform apply -auto-approve
cat output/app.env
cat output/reverse_proxy.conf
```

# os arquivos gerados ficam em terraform/output/  

### 6.3 Windows (PowerShell)

```powershell
# 1. Clonar o repositório
git clone https://github.com/<seu-usuario>/devsecops-scan.git
cd devsecops-scan

# 2. Criar e ativar um ambiente virtual
python -m venv venv
venv\Scripts\Activate.ps1

# 3. Instalar as dependências da aplicação
pip install -r requirements.txt

# 4. Rodar os testes automatizados
pytest -v --cov=app

# 5. Subir a aplicação localmente
python run.py
# A API fica disponível em http://localhost:5000
```

**Instalando e rodando o Semgrep (SAST):**

```powershell
pip install semgrep
semgrep scan --config auto
```

> O Semgrep roda via WSL de forma mais estável no Windows. Caso a
> instalação via `pip` apresente problemas, instale o WSL
> (`wsl --install`) e rode os comandos acima dentro dele.

**Instalando e rodando o pip-audit (SCA):**

```powershell
pip install pip-audit
pip-audit -r requirements.txt
```

**Rodando o OWASP ZAP (DAST) via Docker Desktop:**

```powershell
# com a aplicação já rodando em outro terminal (python run.py)
docker run -t --network="host" ghcr.io/zaproxy/zaproxy:stable `
  zap-baseline.py -t http://localhost:5000
```

> O modo `--network="host"` não é suportado nativamente pelo Docker
> Desktop no Windows. Nesse caso, use o IP da máquina
> (`ipconfig`, geralmente algo como `192.168.x.x`) no lugar de
> `localhost`, ou rode o ZAP Desktop (interface gráfica) apontando
> para `http://localhost:5000`.

**Rodando o Terraform:**

```powershell
cd terraform
terraform init
terraform validate
terraform plan
terraform apply -auto-approve
Get-Content output\app.env
Get-Content output\reverse_proxy.conf
```

> Observação: a captura oficial dos prints desta entrega foi feita no
> Linux, seguindo exatamente os comandos da seção 6.2.

---

## 7. Conclusão

Esta prática proposta pela atividade aplica **DevSecOps** ao incorporar ferramentas de
segurança diretamente no pipeline de CI/CD, em vez de tratá-las como
uma etapa manual e separada do desenvolvimento. E aplica
especificamente o conceito de **Shift Left** porque:

- A análise de **SAST** (Semgrep) roda sobre o código-fonte antes
  mesmo de qualquer deploy, pegando problemas no momento em que o
  código é escrito/commitado.
- A análise de **SCA** (pip-audit) verifica as dependências assim que
  o `requirements.txt` muda, evitando que uma biblioteca vulnerável
  chegue a produção.
- A análise de **DAST** (OWASP ZAP), mesmo sendo uma verificação em
  tempo de execução, acontece ainda dentro da pipeline de CI - antes
  de qualquer merge na branch principal - e não depois que a
  aplicação já está no ar para usuários reais.
- A infraestrutura (**Terraform** + **Trivy**) também é validada e
  escaneada por segurança antes de ser considerada pronta, aplicando
  o mesmo princípio de "encontrar o problema o quanto antes" também
  no nível de infraestrutura.

Com isso, qualquer alteração de código só chega à branch principal
depois de passar por quatro camadas de verificação de segurança
automatizadas, sem depender de um processo manual de revisão de
segurança no final do ciclo.
