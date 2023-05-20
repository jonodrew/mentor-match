import aws_cdk as cdk
from aws_cdk import aws_ec2 as ec2, aws_ecs as ecs, aws_autoscaling as autoscaling, aws_ecs_patterns as ecs_patterns
from constructs import Construct

class MentorMatchStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(
            self, "MentorMatchVPC", max_azs=1
        )

        cluster = ecs.Cluster(self, "EC2Cluster", vpc=vpc)

        autoscaling_group = autoscaling.AutoScalingGroup(
            self, "DefaultAutoScalingGroup",
            instance_type=ec2.InstanceType("t2.nano"),
            machine_image=ecs.EcsOptimizedImage.amazon_linux2(),
            vpc=vpc,
        )

        capacity_provider = ecs.AsgCapacityProvider(self, "AsgCapacityProvider",
            auto_scaling_group=autoscaling_group
        )
        cluster.add_asg_capacity_provider(capacity_provider)

        ecs_service = ecs_patterns.NetworkLoadBalancedEc2Service(
            self, "Ec2Service",
            cluster=cluster,
            memory_limit_mib=256,
            task_image_options=ecs_patterns.NetworkLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_registry("ghcr.io/mentor-matching-online/mentor-match/web")
            )
        )

        autoscaling_group.connections.allow_from_any_ipv4(port_range=ec2.Port.tcp_range(32768, 65535),
                                            description="allow incoming traffic from ALB")

        cdk.CfnOutput(
            self, "LoadBalancerDNS",
            value="http://" + ecs_service.load_balancer.load_balancer_dns_name
        )
