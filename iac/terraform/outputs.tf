output "apprunner_service_url" {
  value = aws_apprunner_service.mmweb.service_url
}
output "aws_apprunner_service_domain_name" {
  value = aws_apprunner_custom_domain_association.mmweb.domain_name
}

output "certificate_records" {
  value = aws_apprunner_custom_domain_association.mmweb.certificate_validation_records
}

output "dns_target" {
  value = aws_apprunner_custom_domain_association.mmweb.dns_target

}