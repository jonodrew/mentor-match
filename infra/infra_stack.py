from aws_cdk import Stack, aws_lambda_python_alpha as lambda_python
from aws_cdk.aws_lambda import Runtime
from constructs import Construct


class ProcessData(Construct):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super(ProcessData, self).__init__(scope=scope, id=id)

        dependencies = lambda_python.PythonLayerVersion(
            scope=self,
            id="MatchProcessingDependencies",
            entry="./lambda/python",
            compatible_runtimes=[Runtime.PYTHON_3_9],
        )
        lambda_python.PythonFunction(
            scope=self,
            id="ProcessDataFunction",
            entry="./lambda",
            runtime=Runtime.PYTHON_3_9,
            index="index.py",
            handler="async_process_data_event_handler",
            layers=[dependencies],
        )


class MentorMatchStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        ProcessData(scope=self, id="DataProcessingStepFunction")
