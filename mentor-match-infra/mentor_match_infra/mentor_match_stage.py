import aws_cdk as cdk
from constructs import Construct
from .infrastructure import MentorMatchStack


class MentorMatchAppStage(cdk.Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        service = MentorMatchStack(self, "MentorMatchStack")

