import aws_cdk as cdk
from aws_cdk.aws_ecs import ContainerImage
from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedFargateService, ApplicationLoadBalancedTaskImageOptions
from constructs import Construct


class MentorMatchStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, image_tag: str = "latest", **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ApplicationLoadBalancedFargateService(self, "MentorMatchWebServer",cpu=256, memory_limit_mib=512, listener_port=80,
                                              task_image_options=ApplicationLoadBalancedTaskImageOptions(
                                                  image=ContainerImage.from_registry(
                                                      f"ghcr.io/mentor-matching-online/mentor-match/web:{image_tag}"),
                                                  public_load_balancer=True,
                                              )
                                              )
