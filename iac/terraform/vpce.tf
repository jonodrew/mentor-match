resource "aws_security_group" "allow_access_to_vpce" {
  name        = "allow_vpce"
  description = "Allow vpce https inbound traffic and egress anywhere"
  vpc_id      = module.vpc.vpc_id

  ingress {
    description = "https from VPC"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [module.vpc.vpc_cidr_block]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name        = "allow_vpce_from_vpc"
    Terraform   = "true"
    Environment = "dev"
    Project     = "mentor-match"
  }
}

resource "aws_vpc_endpoint" "ecr_api" {
  service_name        = "com.amazonaws.${data.aws_region.current.name}.ecr.api"
  private_dns_enabled = true
  vpc_id              = module.vpc.vpc_id
  subnet_ids          = module.vpc.intra_subnets
  security_group_ids  = [aws_security_group.allow_access_to_vpce.id]
  tags = {
    Name        = "ecr_api"
    Terraform   = "true"
    Environment = "dev"
    Project     = "mentor-match"
  }
  vpc_endpoint_type = "Interface"
  auto_accept       = true
}

resource "aws_vpc_endpoint" "ecr_dkr" {
  service_name        = "com.amazonaws.${data.aws_region.current.name}.ecr.dkr"
  private_dns_enabled = true
  vpc_id              = module.vpc.vpc_id
  subnet_ids          = module.vpc.intra_subnets
  security_group_ids  = [aws_security_group.allow_access_to_vpce.id]
  tags = {
    Name        = "ecr_dkr"
    Terraform   = "true"
    Environment = "dev"
    Project     = "mentor-match"
  }
  vpc_endpoint_type = "Interface"
  auto_accept       = true
}

resource "aws_vpc_endpoint" "ecs_agent" {
  service_name        = "com.amazonaws.${data.aws_region.current.name}.ecs-agent"
  private_dns_enabled = true
  vpc_id              = module.vpc.vpc_id
  subnet_ids          = module.vpc.intra_subnets
  security_group_ids  = [aws_security_group.allow_access_to_vpce.id]
  tags = {
    Name        = "ecs_agent"
    Terraform   = "true"
    Environment = "dev"
    Project     = "mentor-match"
  }
  vpc_endpoint_type = "Interface"
  auto_accept       = true
}
resource "aws_vpc_endpoint" "ecs_telemetry" {
  service_name        = "com.amazonaws.${data.aws_region.current.name}.ecs-telemetry"
  private_dns_enabled = true
  vpc_id              = module.vpc.vpc_id
  subnet_ids          = module.vpc.intra_subnets
  security_group_ids  = [aws_security_group.allow_access_to_vpce.id]
  tags = {
    Name        = "ecs_telemetry"
    Terraform   = "true"
    Environment = "dev"
    Project     = "mentor-match"
  }
  vpc_endpoint_type = "Interface"
  auto_accept       = true
}
resource "aws_vpc_endpoint" "ecs" {
  service_name        = "com.amazonaws.${data.aws_region.current.name}.ecs"
  private_dns_enabled = true
  vpc_id              = module.vpc.vpc_id
  subnet_ids          = module.vpc.intra_subnets
  security_group_ids  = [aws_security_group.allow_access_to_vpce.id]
  tags = {
    Name        = "ecs"
    Terraform   = "true"
    Environment = "dev"
    Project     = "mentor-match"
  }
  vpc_endpoint_type = "Interface"
  auto_accept       = true
}

resource "aws_vpc_endpoint" "cloudwatch" {
  service_name        = "com.amazonaws.${data.aws_region.current.name}.logs"
  private_dns_enabled = true
  vpc_id              = module.vpc.vpc_id
  subnet_ids          = module.vpc.intra_subnets
  security_group_ids  = [aws_security_group.allow_access_to_vpce.id]
  tags = {
    Name        = "cloudwatch"
    Terraform   = "true"
    Environment = "dev"
    Project     = "mentor-match"
  }
  vpc_endpoint_type = "Interface"
  auto_accept       = true
}

resource "aws_vpc_endpoint" "s3" {
  service_name    = "com.amazonaws.${data.aws_region.current.name}.s3"
  vpc_id          = module.vpc.vpc_id
  route_table_ids = module.vpc.intra_route_table_ids
  tags = {
    Name        = "s3"
    Terraform   = "true"
    Environment = "dev"
    Project     = "mentor-match"
  }
  vpc_endpoint_type = "Gateway"
  auto_accept       = true

}