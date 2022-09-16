data "aws_iam_policy_document" "ecs_exec_role_trust" {
  statement {
    actions = [
      "sts:AssumeRole"
    ]
    principals {
      type        = "Service"
      identifiers = ["ecs.amazonaws.com", "ecs-tasks.amazonaws.com"]
    }
    effect = "Allow"
  }
}

resource "aws_iam_role" "ecs_celery_exec_role" {
  name               = "ecs_celery_exec_role"
  assume_role_policy = data.aws_iam_policy_document.ecs_exec_role_trust.json
}

resource "aws_iam_role_policy_attachment" "ecs_celery_exec_role" {
  role       = aws_iam_role.ecs_celery_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}
resource "aws_iam_role_policy_attachment" "ecs_celery_ecr_pull" {
  role       = aws_iam_role.ecs_celery_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

resource "aws_ecs_cluster" "celery" {
  name = "celery-workers"
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
  tags = {
    Name        = "mentor-match-ecs-cluster"
    Terraform   = "true"
    Environment = "dev"
    Project     = "mentor-match"
  }
}

resource "aws_cloudwatch_log_group" "ecs_logs" {
  name              = "/ecs/mmweb-celery/worker"
  retention_in_days = 30
  tags = {
    Name        = "mentor-match-worker-ecs-logs"
    Terraform   = "true"
    Environment = "dev"
    Project     = "mentor-match"
  }
}

resource "aws_ecs_task_definition" "celery_worker" {
  family                   = "mentor-match-worker"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_celery_exec_role.arn
  task_role_arn            = aws_iam_role.ecs_celery_exec_role.arn
  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "X86_64"
  }
  container_definitions = jsonencode(
    [
      {
        name      = "worker"
        image     = var.worker_image_uri
        cpu       = 256
        memory    = 512
        user      = "nobody"
        privileged = false
        essential = true
        environment = [
          {
          name  = "SERVICE_URL"
          value = "https://${aws_apprunner_service.mmweb.service_url}"
          },
          {
            name = "FLASK_ENV"
            value = "development"
          },
          {
            name = "REDIS_URL"
            value = "redis://${aws_elasticache_cluster.redis.cache_nodes.0.address}:${aws_elasticache_cluster.redis.cache_nodes.0.port}/0"
          }
        ]
        logConfiguration = {
          logDriver = "awslogs"
          options = {
            "awslogs-group"         = aws_cloudwatch_log_group.ecs_logs.name
            "awslogs-region"        = data.aws_region.current.name
            "awslogs-stream-prefix" = "worker"
          }
        }
      }
    ]
  )
  tags = {
    Name        = "mentor-match-worker"
    Terraform   = "true"
    Environment = "dev"
    Project     = "mentor-match"
  }

}

resource "aws_ecs_service" "worker" {
  name                = "mentor-match-worker"
  cluster             = aws_ecs_cluster.celery.id
  task_definition     = aws_ecs_task_definition.celery_worker.arn
  desired_count       = 1
  scheduling_strategy = "REPLICA"
  launch_type         = "FARGATE"
  platform_version    = "LATEST"
  propagate_tags      = "TASK_DEFINITION"
  tags = {
    Name        = "mentor-match-worker-service"
    Terraform   = "true"
    Environment = "dev"
    Project     = "mentor-match"
  }
  network_configuration {
    subnets          = module.vpc.intra_subnets
    security_groups  = [aws_security_group.allow_redis_from_vpc.id]
    assign_public_ip = false
  }



}