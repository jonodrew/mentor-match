import aws_cdk as cdk
import aws_cdk.aws_ecs as ecs
import aws_cdk.aws_ecs_patterns as ecsp
from constructs import Construct


class MentorMatchStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ecsp.ApplicationLoadBalancedFargateService(
            self,
            "MentorMatchWeb",
            task_image_options=ecsp.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_registry(
                    "ghcr.io/mentor-matching-online/mentor-match/web"
                )
            ),
            public_load_balancer=True,
        )
        ecsp.ApplicationLoadBalancedFargateService(
            self,
            "MentorMatchWorker",
            task_image_options=ecsp.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_registry(
                    "ghcr.io/mentor-matching-online/mentor-match/worker"
                )
            ),
            public_load_balancer=True,
        )
