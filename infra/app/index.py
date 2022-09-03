from typing import Callable, Union, Any

import json
import os
import boto3

from helpers import serialize, deserialize
from tasks import (
    async_process_data,
    Result,
    prepare_data_iterator,
    reduce_to_best_output,
)
from classes import CSMentee, CSMentor


def s3_resource():
    return boto3.resource("s3")


bucket_name = os.environ.get("S3_BUCKET_NAME")

mappable_func = Callable[[list[CSMentor], list[CSMentee], int], Result]


def serialize_deserialize(
    function: mappable_func,
) -> Callable[[dict, Any], dict[str, Union[list[dict], int]]]:
    def wrapped_func(event: dict, context) -> dict[str, Union[list[dict], int]]:
        inputs = deserialize(event)

        output = function(*inputs)

        return serialize(*output)

    return wrapped_func


def read_write_s3(function: Callable[[dict, Any], Union[dict, list]]):
    def wrapped_func(event: dict, context) -> dict[str, Union[str, int]]:
        data_uuid = event["data_uuid"]
        step = event.get("step", 0)
        data = s3_resource().Object(bucket_name, f"{data_uuid}/{str(step)}.json")
        file_content = data.get()["Body"].read().decode("utf-8")
        json_content = json.loads(file_content)

        output = function(json_content, context)

        data_for_next_step = s3_resource().Object(
            bucket_name, f"{data_uuid}/{str(step + 1)}"
        )
        data_for_next_step.put(Body=(bytes(json.dumps(output).encode("UTF-8"))))
        return {"data_uuid": data_uuid, "step": step + 1}

    return wrapped_func


def async_process_data_event_handler(event: dict[str, Union[str, int]], context):
    """
    Event handler that calls the `tasks.async_process_data` function.
    :param event: A dictionary with an event from AWS. Must have the "mentees" and "mentors" keys
    :param context: The AWS context
    :return:
    """
    return read_write_s3(serialize_deserialize(async_process_data))(event, context)


def find_best_result_lambda(event: dict, context):
    """
    Event handler to find the "best" unmatched bonus value. See `tasks.find_best_output` for implementation details
    :param event: The triggering event. An array that should consist of
    {"mentor": [...], "mentee": [...], "unmatched bonus": int} dicts
    :param context: The AWS context
    :return: A single {"mentor": [...], "mentee": [...], "unmatched bonus": int} dict
    """
    ...


def prepare_data_for_mapping(event: dict, context):
    """
    Create fresh copies of data, ready for handing to the mapping State defined in the infrastructure
    :param event: The data to be matched
    :param context: The AWS context
    :return: A list of dicts with the format {"mentor": [...], "mentee": [...], "unmatched bonus": int}
    """

    def _prepare_data(data: dict) -> list[dict]:
        prepared_data = prepare_data_iterator(*deserialize(data))
        return [serialize(*result) for result in prepared_data]

    return read_write_s3(_prepare_data)(event, context)
