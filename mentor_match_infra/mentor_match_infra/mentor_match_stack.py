import aws_cdk as cdk
from aws_cdk import aws_ec2 as ec2, aws_ecs as ecs
from aws_cdk.aws_ecs import ContainerImage
from aws_cdk.aws_ecs_patterns import (
    ApplicationLoadBalancedFargateService,
    ApplicationLoadBalancedTaskImageOptions,
)
from aws_cdk.aws_sqs import Queue
from constructs import Construct


class MentorMatchStack(cdk.Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        image_tag: str = "latest",
        debug: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self, "MentorMatchVPC", max_azs=3)  # default is all AZs in region

        cluster = ecs.Cluster(self, "MentorMatchCluster", vpc=vpc)

        broker_vars = {"broker_url": "sqs://"}

        web_service = ApplicationLoadBalancedFargateService(
            self,
            "MentorMatchWebServer",
            cpu=256,
            memory_limit_mib=512,
            listener_port=80,
            public_load_balancer=True,
            cluster=cluster,
            desired_count=1,
            task_image_options=ApplicationLoadBalancedTaskImageOptions(
                image=ContainerImage.from_registry(
                    f"ghcr.io/mentor-matching-online/mentor-match/web:{image_tag}"
                ),
                container_port=80,
                environment={"FLASK_DEBUG": "1" if debug else "0", **broker_vars},
            ),
        )
        web_service.target_group.configure_health_check(path="/login")

        celery_worker = ApplicationLoadBalancedFargateService(
            self,
            "MentorMatchCeleryWorker",
            cpu=256,
            memory_limit_mib=512,
            assign_public_ip=False,
            cluster=cluster,
            desired_count=1,
            task_image_options=ApplicationLoadBalancedTaskImageOptions(
                image=ContainerImage.from_registry(
                    f"ghcr.io/mentor-matching-online/mentor-match/worker:{image_tag}"
                ),
                environment=broker_vars,
            ),
        )

        broker = Queue(self, "MentorQueue")

        broker.grant_send_messages(celery_worker.task_definition.task_role)
        broker.grant_consume_messages(celery_worker.task_definition.task_role)

        broker.grant_consume_messages(web_service.task_definition.task_role)
        broker.grant_send_messages(web_service.task_definition.task_role)
