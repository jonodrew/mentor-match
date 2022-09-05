terraform {
  required_version = ">= 0.12.2"

  backend "s3" {
    region         = "eu-west-1"
    bucket         = "iac-dev-mentor-match-state"
    key            = "terraform.tfstate"
    dynamodb_table = "iac-dev-mentor-match-state-lock"
    profile        = ""
    role_arn       = ""
    encrypt        = "true"
  }
}
