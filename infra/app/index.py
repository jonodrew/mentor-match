from typing import Callable, Union, Any, TypedDict, Sequence

import json
import os
import boto3

from helpers import serialize, deserialize, read_from_s3, write_to_s3, TaskIO
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


def read_write_s3(function: Callable[[dict, Any], Union[dict, list]]) -> Callable[[dict, Any], TaskIO]:
    def wrapped_func(event: dict, context) -> TaskIO:
        json_content = read_from_s3(event, s3_resource(), bucket_name)

        output = function(json_content, context)

        return write_to_s3(s3_resource(), bucket_name, event["step"], event["data_uuid"], output)

    return wrapped_func


def async_process_data_event_handler(event: TaskIO, context) -> TaskIO:
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


def prepare_data_for_mapping(event: dict, context) -> Sequence[TaskIO]:
    """
    Create fresh copies of data, ready for handing to the mapping State defined in the infrastructure
    :param event: The data to be matched
    :param context: The AWS context
    :return: A list of dicts with the format {"mentor": [...], "mentee": [...], "unmatched bonus": int}
    """
    def _prepare_data(data) -> list[dict[str, list[dict] | int]]:
        prepare_data_for_mapping.hello = "hello"
        mentors, mentees, bonus = deserialize(data)
        prepared_data = prepare_data_iterator(mentors, mentees)
        return [serialize(*result) for result in prepared_data]

    prepared_data = _prepare_data(read_from_s3(event, s3_resource(), bucket_name))
    write_to_s3(s3_resource(), bucket_name, event["step"], event["data_uuid"], prepared_data)
    return [TaskIO(data_uuid=event["data_uuid"])]


