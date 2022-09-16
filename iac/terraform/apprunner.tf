resource "aws_iam_role" "mmweb_build" {
  name               = "mmweb-build"
  assume_role_policy = <<EOF
    {
    "Version": "2012-10-17",
    "Statement": [
        {
        "Sid": "",
        "Effect": "Allow",
        "Principal": {
            "Service": "build.apprunner.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
        }
    ]
}
EOF
}
resource "aws_iam_role_policy_attachment" "mmweb_build" {
  role       = aws_iam_role.mmweb_build.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess"

}

resource "aws_iam_policy" "exec_policy" {
  name        = "duplicate-slr-policy"
  description = "duplicates the service linked role policy"
  policy      = data.aws_iam_policy_document.apprunner_exec_policy.json
}

resource "aws_iam_role" "mmweb_exec" {
  name               = "mmweb-exec"
  assume_role_policy = <<EOF
    {
    "Version": "2012-10-17",
    "Statement": [
        {
        "Sid": "",
        "Effect": "Allow",
        "Principal": {
            "Service": "tasks.apprunner.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "mmweb_exec" {
  role       = aws_iam_role.mmweb_exec.name
  policy_arn = aws_iam_policy.exec_policy.arn
}

resource "aws_security_group" "apprunner" {
  name        = "apprunner"
  description = "Allow egress to redis"
  vpc_id      = module.vpc.vpc_id

  egress {
    from_port       = aws_elasticache_cluster.redis.cache_nodes.0.port
    to_port         = aws_elasticache_cluster.redis.cache_nodes.0.port
    protocol        = "tcp"
    security_groups = [aws_security_group.allow_redis_from_vpc.id]

  }

  tags = {
    Name        = "allow_apprunner_to_redis_in_vpc"
    Terraform   = "true"
    Environment = "dev"
    Project     = "mentor-match"
  }
}


resource "aws_apprunner_vpc_connector" "connector" {
  vpc_connector_name = "mm-vpc-connector"
  subnets            = module.vpc.intra_subnets
  security_groups    = [aws_security_group.allow_redis_from_vpc.id]

  tags = {
    Terraform   = "true"
    Environment = "dev"
    Project     = "mentor-match"
  }
}


resource "aws_apprunner_service" "mmweb" {
  service_name = "mmweb"
  instance_configuration {
    cpu               = 1024
    memory            = 2048
    instance_role_arn = aws_iam_role.mmweb_exec.arn
  }
  source_configuration {
    authentication_configuration {
      access_role_arn = aws_iam_role.mmweb_build.arn
    }
    image_repository {
      image_configuration {
        port = "5000"
        runtime_environment_variables = {
          "FLASK_APP" = "app:create_app()"
          "FLASK_ENV" = "development"
          "REDIS_URL" = "redis://${aws_elasticache_cluster.redis.cache_nodes.0.address}:${aws_elasticache_cluster.redis.cache_nodes.0.port}/0"
        }
      }
      image_identifier      = var.application_image_uri
      image_repository_type = "ECR"
    }
    auto_deployments_enabled = false
  }
  network_configuration {
    egress_configuration {
      egress_type       = "VPC"
      vpc_connector_arn = aws_apprunner_vpc_connector.connector.arn
    }

  }


  tags = {
    Name = "mmweb-apprunner-service"
  }
}
