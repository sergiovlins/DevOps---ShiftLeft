variable "app_name" {
  description = "Nome da aplicação, usado nos arquivos de configuração gerados."
  type        = string
  default     = "devsecops-scan"
}

variable "app_port" {
  description = "Porta em que a aplicação Flask escuta."
  type        = number
  default     = 5000
}

variable "environment" {
  description = "Ambiente alvo (development, staging, production)."
  type        = string
  default     = "production"
}
