from aws_cdk import Stack, Environment, Stage
from aws_cdk.pipelines import CodePipeline, ShellStep, CodePipelineSource, ManualApprovalStep
from aws_cdk.aws_codepipeline_actions import CloudFormationDeleteStackAction
from constructs import Construct
from .mentor_match_stage import MentorMatchAppStage




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
        testing_stage = MentorMatchAppStage(self, "testing", env=Environment(account="712310211354", region="eu-west-2"))
        testing_stage_deployment = pipeline.add_stage(testing_stage)
        testing_stage_deployment.add_post(
            ShellStep(
                "Delete", commands=[
                    "npm install -g aws-cdk",
                    "cd mentor-match-infra",
                    "python -m pip install -r requirements.txt",
                    "cdk ls",
                    f"cdk destroy {construct_id}/{testing_stage.stage_name}/{testing_stage_deployment.stacks.pop().stack_name} --force"
                ]
            )
        )
        # testing_stage_deployment.add_action(
        #     CloudFormationDeleteStackAction(
        #         admin_permissions=True,
        #         stack_name=testing_stage_deployment.stacks.pop().stack_name,
        #         action_name="delete test stack"
        # ))

        # testing_stage.add_action(
        #     CloudFormationDeleteStackAction(
        #         admin_permissions=True,
        #         stack_name=testing_stage_deployment.stacks.pop().stack_name,
        #         action_name="delete test stack"
        #     )
        # )

        production_stage = pipeline.add_stage(
            MentorMatchAppStage(self, "production", env=Environment(account="712310211354", region="eu-west-2"))
        )
        production_stage.add_pre(
            ManualApprovalStep('approval')
        )
