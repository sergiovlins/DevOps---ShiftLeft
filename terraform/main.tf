# Infraestrutura como Código do projeto "DevOps - Prática Shift-Left".
# Usa o provider "local" (sem nuvem, credenciais ou custo) para gerar
# os arquivos de configuração do ambiente de produção.

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

# Variáveis de ambiente da aplicação (apenas valores não sensíveis).
resource "local_file" "app_env_config" {
  filename = "${path.module}/output/app.env"
  content  = <<-EOT
    FLASK_ENV=${var.environment}
    APP_NAME=${var.app_name}
    APP_PORT=${var.app_port}
    FLASK_DEBUG=false
  EOT
}

# Proxy reverso (Nginx) com cabeçalhos de segurança.
resource "local_file" "reverse_proxy_conf" {
  filename = "${path.module}/output/reverse_proxy.conf"
  content  = <<-EOT
    server {
        listen 80;
        server_name ${var.app_name};

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
