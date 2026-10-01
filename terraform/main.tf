# ------------------------------------------------------------------
# Terraform - Infraestrutura como Código do projeto devsecops-scan
#
# O objetivo desta atividade é demonstrar segurança no ciclo de
# desenvolvimento (Shift Left), não a implantação em um provedor de
# nuvem real. Por isso uso aqui o provider "local" do Terraform: ele
# não exige credenciais de nuvem, não gera custo e não depende de
# subir uma imagem Docker - mas ainda assim demonstra, de forma
# real, o conceito de Infraestrutura como Código: o estado final do
# ambiente (os arquivos de configuração que a aplicação usaria em
# produção) é descrito de forma declarativa e gerado automaticamente
# pelo Terraform a partir deste código.
# ------------------------------------------------------------------

terraform {
  required_version = ">= 1.6.0"

  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
  }
}

provider "local" {}

# Representa o arquivo de variáveis de ambiente que a aplicação
# Flask consumiria em produção. Em um cenário real, segredos nunca
# seriam versionados em texto puro (viriam de um Secrets Manager) -
# aqui, para fins didáticos, uso apenas valores não sensíveis.
resource "local_file" "app_env_config" {
  filename = "${path.module}/output/app.env"
  content  = <<-EOT
    FLASK_ENV=${var.environment}
    APP_NAME=${var.app_name}
    APP_PORT=${var.app_port}
    # Flag que indica que o deploy final já nasce com a aplicação
    # rodando sem o modo debug do Flask ativado (boa prática de
    # segurança cobrada pelo próprio SAST na etapa anterior).
    FLASK_DEBUG=false
  EOT
}

# Representa a configuração de um proxy reverso (ex.: Nginx) na
# frente da aplicação, já endurecida (hardened) com cabeçalhos de
# segurança recomendados. Isso simula o "estado final" da infra que
# protegeria a aplicação em produção, sem precisar efetivamente subir
# um container Docker para esta atividade.
resource "local_file" "reverse_proxy_conf" {
  filename = "${path.module}/output/reverse_proxy.conf"
  content  = <<-EOT
    server {
        listen 80;
        server_name ${var.app_name};

        # Cabeçalhos de segurança (mitigam clickjacking, MIME
        # sniffing, XSS refletido e vazamento de informação via
        # Referrer) - decisão de infraestrutura que complementa as
        # análises de SAST/SCA/DAST feitas sobre a aplicação em si.
        add_header X-Frame-Options "DENY";
        add_header X-Content-Type-Options "nosniff";
        add_header X-XSS-Protection "1; mode=block";
        add_header Referrer-Policy "strict-origin-when-cross-origin";

        location / {
            proxy_pass http://127.0.0.1:${var.app_port};
        }
    }
  EOT
}
