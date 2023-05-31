from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_elasticache as elasticache,
    CfnOutput,
)
from constructs import Construct

app_port = 8008


class ElasticacheDemoCdkAppStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPC
        vpc = ec2.Vpc(
            self,
            "VPC",
            nat_gateways=1,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public", subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="private",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24,
                ),
            ],
        )

        # Security Groups
        webserver_sec_group = ec2.SecurityGroup(
            self,
            "webserver_sec_group",
            security_group_name="webserver_sec_group",
            vpc=vpc,
            allow_all_outbound=True,
        )
        redis_sec_group = ec2.SecurityGroup(
            self,
            "redis-sec-group",
            security_group_name="redis-sec-group",
            vpc=vpc,
            allow_all_outbound=True,
        )

        private_subnets_ids = [ps.subnet_id for ps in vpc.private_subnets]

        redis_subnet_group = elasticache.CfnSubnetGroup(
            scope=self,
            id="redis_subnet_group",
            subnet_ids=private_subnets_ids,  # todo: add list of subnet ids here
            description="subnet group for redis",
        )

        # Add ingress rules to security group
        webserver_sec_group.add_ingress_rule(
            peer=ec2.Peer.ipv4("0.0.0.0/0"),
            description="Flask Application",
            connection=ec2.Port.tcp(app_port),
        )

        redis_sec_group.add_ingress_rule(
            peer=webserver_sec_group,
            description="Allow Redis connection",
            connection=ec2.Port.tcp(6379),
        )

        # Elasticache for Redis cluster
        redis_cluster = elasticache.CfnCacheCluster(
            scope=self,
            id="redis_cluster",
            engine="redis",
            cache_node_type="cache.t2.micro",
            num_cache_nodes=1,
            cache_subnet_group_name=redis_subnet_group.ref,
            vpc_security_group_ids=[redis_sec_group.security_group_id],
        )

        # AMI definition
        amzn_linux = ec2.MachineImage.latest_amazon_linux(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2
        )

        # Instance Role and SSM Managed Policy
        role = iam.Role(
            self,
            "ElasticacheDemoInstancePolicy",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
        )
        role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonSSMManagedInstanceCore"
            )
        )
        role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "AWSCloudFormationReadOnlyAccess"
            )
        )

        # The following inline policy makes sure we allow only retrieving the secret value, provided the secret is already known.
        # It does not allow listing of all secrets.
        role.attach_inline_policy(
            iam.Policy(
                self,
                "secret-read-only",
                statements=[
                    iam.PolicyStatement(
                        actions=["secretsmanager:GetSecretValue"],
                        resources=["arn:aws:secretsmanager:*"],
                        effect=iam.Effect.ALLOW,
                    )
                ],
            )
        )

        # EC2 Instance for Web Server
        instance = ec2.Instance(
            self,
            "WebServer",
            instance_type=ec2.InstanceType("t3.small"),
            machine_image=amzn_linux,
            vpc=vpc,
            role=role,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            security_group=webserver_sec_group,
        )

        # Generate CloudFormation Outputs
        CfnOutput(
            scope=self,
            id="redis_endpoint",
            value=redis_cluster.attr_redis_endpoint_address,
        )
        CfnOutput(
            scope=self, id="webserver_public_ip", value=instance.instance_public_ip
        )
        CfnOutput(
            scope=self,
            id="webserver_public_url",
            value=instance.instance_public_dns_name,
        )
