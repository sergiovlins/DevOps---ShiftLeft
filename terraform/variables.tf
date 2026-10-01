variable "app_name" {
  description = "Nome da aplicação, sem espaços ou acentos (usado como server_name)."
  type        = string
  default     = "devops-pratica-shift-left"
}

variable "app_port" {
  description = "Porta da aplicação Flask."
  type        = number
  default     = 5000
}

variable "environment" {
  description = "Ambiente alvo: development, staging ou production."
  type        = string
  default     = "production"
}
