from aws_cdk import Stack
from aws_cdk.pipelines import CodePipeline, ShellStep, CodePipelineSource
from constructs import Construct


class MentorMatchPipeline(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        pipeline = CodePipeline(self, "MentorMatchPipeline",
                                pipeline_name="Pipeline",
                                synth=ShellStep("Synth",
                                                input=CodePipelineSource.git_hub("mentor-matching-online/mentor-match", "main"),
                                                commands=["npm install -g aws-cdk",
                                                          "cd mentor-match-infra",
                                                          "python -m pip install -r requirements.txt",
                                                          "cdk synth"],
                                                primary_output_directory="mentor-match-infra/cdk.out"
                                                )
                                )
