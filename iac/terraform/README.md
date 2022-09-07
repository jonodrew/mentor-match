Infrastructure as Code - Terraform for Mentor Match Deployment
===============================================================

Services used: 

* AWS Elasticache
* AWS App Runner
* AWS Elastic Container Repositories (ECR)
* AWS Elastic Container Services (ECS)
* Route 53

Using this code:
---------------

1. Create a Route53 Hosted Zone for your domain (not included in the terraform because reasons.)
2. Create somewhere to host the docker images for `mentor-match-app` and `mentor-match-worker`.  I used AWS ECR, and VPC Endpoints for isolated subnets to be able to access them. If you were using Docker Hub, you'd want to change some stuff to host the application either in Public subnets, or Private with a NAT gateway. 
3. Create a .tfvars file containing definitions for the variables `hosted_zone_id`, `application_image_uri` and `worker_image_uri`. 
4. Run terraform to provision the infrastructure.
