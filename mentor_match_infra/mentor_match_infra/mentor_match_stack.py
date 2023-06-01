import aws_cdk as cdk
from aws_cdk import aws_ec2 as ec2, aws_ecs as ecs
from aws_cdk.aws_ecs import ContainerImage
from aws_cdk.aws_ecs_patterns import (
    ApplicationLoadBalancedFargateService,
    ApplicationLoadBalancedTaskImageOptions,
)
from aws_cdk.aws_elasticache import CfnCacheCluster, CfnSubnetGroup
from aws_cdk.aws_iam import Role, CompositePrincipal, ArnPrincipal, ManagedPolicy
from constructs import Construct


class DeveloperRole(Role):
    def __init__(self, scope: Construct, id: str):
        principals_to_assume = CompositePrincipal(
            *[
                ArnPrincipal(f"arn:aws:iam::622626885786:user/{username}")
                for username in ["jonathan.kerr@digital.cabinet-office.gov.uk"]
            ]
        ).with_conditions({"Bool": {"aws:MultiFactorAuthPresent": "true"}})
        managed_policies = [
            ManagedPolicy.from_aws_managed_policy_name("PowerUserAccess")
        ]
        super().__init__(
            scope,
            id,
            assumed_by=principals_to_assume,
            role_name="developer",
            managed_policies=managed_policies,
            description="A powerful role for developers to assume",
        )


class RedisCache(Construct):
    def __init__(self, scope: Construct, id_: str, vpc: ec2.Vpc):
        super().__init__(scope, id_)
        self._redis_sec_group = ec2.SecurityGroup(
            self,
            "redis-sec-group",
            security_group_name="redis-sec-group",
            vpc=vpc,
            allow_all_outbound=True,
        )

        private_subnets_ids = [ps.subnet_id for ps in vpc.private_subnets]

        redis_subnet_group = CfnSubnetGroup(
            scope=self,
            id="redis_subnet_group",
            subnet_ids=private_subnets_ids,
            description="subnet group for redis",
        )

        self._redis_cluster = CfnCacheCluster(
            scope=self,
            id="redis_cluster",
            engine="redis",
            cache_node_type="cache.t2.micro",
            num_cache_nodes=1,
            cache_subnet_group_name=redis_subnet_group.ref,
            vpc_security_group_ids=[self._redis_sec_group.security_group_id],
        )

        self._redis_cluster.add_dependency(redis_subnet_group)

        self._connections = ec2.Connections(
            security_groups=[self._redis_sec_group], default_port=ec2.Port.tcp(6379)
        )

    @property
    def cluster(self):
        return self._redis_cluster

    @property
    def security_group(self):
        return self._redis_sec_group

    @property
    def connections(self):
        return self._connections


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

        DeveloperRole(self, "MentorDev")

        vpc = ec2.Vpc(self, "MentorMatchVPC", max_azs=3)  # default is all AZs in region

        cluster = ecs.Cluster(self, "MentorMatchCluster", vpc=vpc)

        backend = RedisCache(self, "MentorCache", vpc)
        redis_url = f"redis://{backend.cluster.attr_redis_endpoint_address}:{backend.cluster.attr_redis_endpoint_port}"

        broker_vars = {
            "BROKER_URL": redis_url,
            "BACKEND_URL": redis_url,
        }

        web_service = ApplicationLoadBalancedFargateService(
            self,
            "MentorMatchWebServer",
            security_groups=backend.cluster.cache_security_group_names,
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

        backend.connections.allow_from(
            web_service.service.connections, port_range=ec2.Port.tcp(6379)
        )
        backend.connections.allow_from_any_ipv4(port_range=ec2.Port.tcp(6379))

        celery_worker = ApplicationLoadBalancedFargateService(
            self,
            "MentorMatchCeleryWorker",
            security_groups=backend.cluster.cache_security_group_names,
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

        celery_worker.target_group.configure_health_check(path="/login")

        backend.connections.allow_from(
            celery_worker.service.connections, port_range=ec2.Port.tcp(6379)
        )
        backend.connections.allow_from_any_ipv4(port_range=ec2.Port.tcp(6379))
