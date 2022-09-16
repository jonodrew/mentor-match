data "aws_route53_zone" "hosting" {
  zone_id = var.hosted_zone_id
}




resource "aws_apprunner_custom_domain_association" "mmweb" {
  domain_name          = "mmweb.${data.aws_route53_zone.hosting.name}"
  service_arn          = aws_apprunner_service.mmweb.arn
  enable_www_subdomain = false
}



resource "aws_route53_record" "apprunner_web_certificate_validation" {
  count = length(aws_apprunner_custom_domain_association.mmweb.certificate_validation_records)

  name    = aws_apprunner_custom_domain_association.mmweb.certificate_validation_records.*.name[count.index]
  type    = aws_apprunner_custom_domain_association.mmweb.certificate_validation_records.*.type[count.index]
  ttl     = 300
  zone_id = data.aws_route53_zone.hosting.id

  records = [aws_apprunner_custom_domain_association.mmweb.certificate_validation_records.*.value[count.index]]
}