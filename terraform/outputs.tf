output "app_env_config_path" {
  description = "Caminho do arquivo de configuração de ambiente gerado."
  value       = local_file.app_env_config.filename
}

output "reverse_proxy_conf_path" {
  description = "Caminho do arquivo de configuração do proxy reverso gerado."
  value       = local_file.reverse_proxy_conf.filename
}
