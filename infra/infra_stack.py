import functools

from aws_cdk import (
    Stack,
    aws_lambda_python_alpha as lambda_python,
    aws_stepfunctions as step_fn,
    aws_stepfunctions_tasks as sfn_tasks,
    aws_s3 as s3,
    aws_apigateway as api_gw,
)
from aws_cdk.aws_lambda import Runtime
from aws_cdk.aws_s3 import Bucket, BlockPublicAccess
from constructs import Construct


class DataStore(Construct):
    """
    A Construct that contains the S3 bucket where we store data, and the API Gateway that manages it
    """

    def __init__(self, scope: Construct, id: str):
        super(DataStore, self).__init__(scope, id)

        self._bucket = s3.Bucket(
            scope=self, id="DataBucket", block_public_access=BlockPublicAccess.BLOCK_ALL
        )

        s3_function_partial = functools.partial(
            lambda_python.PythonFunction,
            scope=self,
            entry="./lambda",
            runtime=Runtime.PYTHON_3_9,
            index="s3_api_gw.py",
        )

        get_handler = s3_function_partial(
            id="GetDataIntegration", handler="s3_gateway_get"
        )
        post_handler = s3_function_partial(
            id="PostDataIntegration", handler="s3_gateway_post"
        )
        delete_handler = s3_function_partial(
            id="DeleteDataIntegration", handler="s3_gateway_delete"
        )

        self.bucket.grant_put(post_handler)
        self.bucket.grant_read(get_handler)
        self.bucket.grant_delete(delete_handler)

        gateway = api_gw.RestApi(scope=self, id="DataBucketAPI")
        bucket_api = gateway.root.add_resource("data")
        bucket_api.add_method(
            "POST", integration=api_gw.LambdaIntegration(post_handler)
        )

        data_set = bucket_api.add_resource("{data_uuid}")
        data_set.add_method("GET", integration=api_gw.LambdaIntegration(get_handler))
        data_set.add_method(
            "DELETE", integration=api_gw.LambdaIntegration(delete_handler)
        )

    @property
    def bucket(self):
        return self._bucket


class ProcessData(Construct):
    """
    A Construct that contains the StateMachine that processes data requests. The State Machine input might not be able
    to cope with very large datasets, so instead we load the code into a bucket, and start the machine with a reference
    to that bucket
    """

    def __init__(self, scope: Construct, id: str, data_bucket: Bucket, **kwargs):
        # TODO: Add S3 bucket and means for writing and reading to and from it
        super().__init__(scope, id)

        dependencies = lambda_python.PythonLayerVersion(
            scope=self,
            id="MatchProcessingDependencies",
            entry="./python",
            compatible_runtimes=[Runtime.PYTHON_3_9],
        )

        process_data_function = lambda_python.PythonFunction(
            scope=self,
            id="ProcessDataFunction",
            entry="./lambda",
            runtime=Runtime.PYTHON_3_9,
            index="index.py",
            handler="async_process_data_event_handler",
            layers=[dependencies],
            memory_size=1024,
        )

        reduce_function = lambda_python.PythonFunction(
            scope=self,
            id="ReduceToBestResult",
            entry="./lambda",
            runtime=Runtime.PYTHON_3_9,
            index="index.py",
            handler="find_best_result_lambda",
            layers=[dependencies],
        )

        prepare_function = lambda_python.PythonFunction(
            scope=self,
            id="PrepareDataForMapping",
            entry="./lambda",
            runtime=Runtime.PYTHON_3_9,
            index="index.py",
            handler="prepare_data_for_mapping",
            layers=[dependencies],
        )

        for fn in (prepare_function, reduce_function, process_data_function):
            data_bucket.grant_read_write(fn)

        reduce_invocation = sfn_tasks.LambdaInvoke(
            scope=self, id="InvokeReduceFunction", lambda_function=reduce_function
        )

        prepare_task = sfn_tasks.LambdaInvoke(
            scope=self, id="InvokePrepareFunction", lambda_function=prepare_function
        )

        map_tasks = step_fn.Map(
            scope=self,
            id="ProcessEveryUnmatchedBonus",
        )
        invoke_process_data_partial = functools.partial(
            sfn_tasks.LambdaInvoke,
            scope=self,
            # id="InvokeProcessData",
            lambda_function=process_data_function,
        )
        map_tasks.iterator(invoke_process_data_partial(id="InvokeProcessDataMap"))

        quantity_path = prepare_task.next(map_tasks).next(reduce_invocation)

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
        data_store = DataStore(self, "DataStorage")
        ProcessData(self, "DataProcessingStepFunction", data_bucket=data_store.bucket)
