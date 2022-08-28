import functools

from aws_cdk import (
    Stack,
    aws_lambda_python_alpha as lambda_python,
    aws_stepfunctions as step_fn,
    aws_stepfunctions_tasks as sfn_tasks,
)
from aws_cdk.aws_lambda import Runtime
from constructs import Construct


class ProcessData(Construct):
    """
    A Construct that contains the StateMachine that processes data requests
    """

    def __init__(self, scope: Construct, id: str, **kwargs):
        super(ProcessData, self).__init__(scope=scope, id=id)

        dependencies = lambda_python.PythonLayerVersion(
            scope=self,
            id="MatchProcessingDependencies",
            entry="./python",
            compatible_runtimes=[Runtime.PYTHON_3_9],
        )

        process_data = lambda_python.PythonFunction(
            scope=self,
            id="ProcessDataFunction",
            entry="./lambda",
            runtime=Runtime.PYTHON_3_9,
            index="index.py",
            handler="async_process_data_event_handler",
            layers=[dependencies],
        )

        reduce_fn = sfn_tasks.LambdaInvoke(
            scope=self,
            id="InvokeReduceFunction",
            lambda_function=lambda_python.PythonFunction(
                scope=self,
                id="ReduceToBestResult",
                entry="./lambda",
                runtime=Runtime.PYTHON_3_9,
                index="index.py",
                handler="find_best_result_lambda",
                layers=[dependencies],
            ),
        )

        prepare_task = sfn_tasks.LambdaInvoke(
            scope=self,
            id="InvokePrepareFunction",
            lambda_function=lambda_python.PythonFunction(
                scope=self,
                id="PrepareDataForMapping",
                entry="./lambda",
                runtime=Runtime.PYTHON_3_9,
                index="index.py",
                handler="prepare_data_for_mapping",
                layers=[dependencies],
            ),
        )

        map_tasks = step_fn.Map(
            scope=self,
            id="ProcessEveryUnmatchedBonus",
        )
        invoke_process_data_partial = functools.partial(
            sfn_tasks.LambdaInvoke,
            scope=self,
            # id="InvokeProcessData",
            lambda_function=process_data,
        )
        map_tasks.iterator(invoke_process_data_partial(id="InvokeProcessDataMap"))

        quantity_path = prepare_task.next(map_tasks).next(reduce_fn)

        approach_choice = step_fn.Choice(scope=self, id="MatchingApproachChoice")

        definition = approach_choice.when(
            step_fn.Condition.string_equals("$.matching_function", "quantity"),
            quantity_path,
        ).otherwise(invoke_process_data_partial(id="InvokeProcessDataOnce"))

        step_fn.StateMachine(
            scope=self, id="ProcessingStateMachine", definition=definition
        )


class MentorMatchStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        ProcessData(scope=self, id="DataProcessingStepFunction")
