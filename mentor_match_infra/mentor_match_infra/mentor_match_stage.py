from typing import Literal, Mapping

import aws_cdk as cdk
from constructs import Construct

from .mentor_match_stack import MentorMatchStack

Account = Literal["staging", "production"]


class MentorMatchAppStage(cdk.Stage):
    stage_env_vars: Mapping[Account, Mapping] = {"staging": {"debug": True}}

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        account: Account = "staging",
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self._service = MentorMatchStack(
            self, "MentorMatchStack", **self.stage_env_vars[account]
        )

    @property
    def service(self):
        return self._service
