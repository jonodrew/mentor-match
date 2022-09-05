module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "mentor-match-vpc"
  cidr = "10.0.0.0/16"

  azs           = ["eu-west-1a", "eu-west-1b", "eu-west-1c"]
  intra_subnets = ["10.0.1.0/26", "10.0.1.64/26", "10.0.1.128/26"]

  enable_dns_hostnames = true
  enable_dns_support   = true
  enable_nat_gateway = false
  enable_vpn_gateway = false

  tags = {
    Terraform   = "true"
    Environment = "dev"
    Project     = "mentor-match"
  }
}