output "app_env_config_path" {
  description = "Caminho do app.env gerado."
  value       = local_file.app_env_config.filename
}

output "reverse_proxy_conf_path" {
  description = "Caminho do reverse_proxy.conf gerado."
  value       = local_file.reverse_proxy_conf.filename
}
