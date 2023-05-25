import jsii
from aws_cdk import Stack
from aws_cdk.aws_codepipeline import IStage
from aws_cdk.aws_codepipeline_actions import CloudFormationDeleteStackAction
from aws_cdk.pipelines import (
    ICodePipelineActionFactory,
    Step,
    CodePipelineActionFactoryResult,
    CodePipeline,
    StackOutputsMap,
)


@jsii.implements(ICodePipelineActionFactory)
class DeleteStack(Step):
    def __init__(self, stack: Stack):
        super().__init__("DeleteStack")
        self._discover_referenced_outputs({"env": {}})
        self._stack = stack

    def produce_action(
        self,
        stage: IStage,
        *,
        scope,
        action_name,
        run_order,
        variables_namespace=None,
        artifacts,
        fallbackArtifact=None,
        pipeline: CodePipeline,
        codeBuildDefaults=None,
        beforeSelfMutation=None,
        stack_outputs_map: StackOutputsMap,
    ):
        stage.add_action(
            CloudFormationDeleteStackAction(
                admin_permissions=True,
                action_name=action_name,
                stack_name=self._stack.stack_name,
                run_order=run_order,
                variables_namespace=variables_namespace,
            )
        )
        return CodePipelineActionFactoryResult(run_orders_consumed=1)
