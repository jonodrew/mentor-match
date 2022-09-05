resource "aws_elasticache_subnet_group" "redis" {
  name       = "mentor-match-redis-subnets"
  subnet_ids = module.vpc.intra_subnets
  tags = {
    Terraform   = "true"
    Environment = "dev"
    Project     = "mentor-match"
  }
}

resource "aws_security_group" "allow_redis_from_vpc" {
  name        = "allow_redis"
  description = "Allow redis inbound traffic and egress anywhere"
  vpc_id      = module.vpc.vpc_id

  ingress {
    description = "redis from VPC"
    from_port   = 6379
    to_port     = 6379
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
    Name        = "allow_redis_from_vpc"
    Terraform   = "true"
    Environment = "dev"
    Project     = "mentor-match"
  }
}

resource "aws_elasticache_cluster" "redis" {
  cluster_id           = "mentor-match-redis"
  engine               = "redis"
  node_type            = "cache.t4g.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis6.x"
  engine_version       = "6.2"
  port                 = 6379
  subnet_group_name    = aws_elasticache_subnet_group.redis.name
  security_group_ids   = [aws_security_group.allow_redis_from_vpc.id]
  tags = {
    Terraform   = "true"
    Environment = "dev"
    Project     = "mentor-match"
  }
}
resource "random_password" "redis_admin_password" {
  length  = 16
  special = false
  upper   = true
  lower   = true
  numeric = true
}
resource "aws_ssm_parameter" "redis_admin_password" {
  name        = "/mentor-match/redis/password/admin"
  description = "Redis Admin Password for Mentor Match"
  type        = "SecureString"
  value       = random_password.redis_admin_password.result

  tags = {
    Terraform   = "true"
    Environment = "dev"
    Project     = "mentor-match"
  }
}
resource "aws_elasticache_user" "admin" {
  user_id       = "redisadmin"
  user_name     = "redisAdmin"
  access_string = "on ~* &* +@all"
  engine        = "REDIS"
  passwords     = [random_password.redis_admin_password.result]
  tags = {
    Terraform   = "true"
    Environment = "dev"
    Project     = "mentor-match"
  }
}