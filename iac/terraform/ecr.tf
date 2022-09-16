resource "aws_ecr_repository" "mentor_match_worker" {
  name                 = "mentor-match-worker"
  image_tag_mutability = "MUTABLE"
  tags = {
    Terraform   = "true"
    Environment = "dev"
    Project     = "mentor-match-worker"
  }
}

resource "aws_ecr_repository" "mentor_match_web" {
  name                 = "mentor-match-web"
  image_tag_mutability = "MUTABLE"
  tags = {
    Terraform   = "true"
    Environment = "dev"
    Project     = "mentor-match-web"
  }
}
output "repo_url_worker" {
  value = aws_ecr_repository.mentor_match_worker.repository_url
}

output "repo_url_web" {
  value = aws_ecr_repository.mentor_match_web.repository_url
}