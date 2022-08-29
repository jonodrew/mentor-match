import json

import uuid

import os

import boto3

s3_client = boto3.client("s3")
bucket_name = os.environ.get("S3_BUCKET_NAME")


def s3_gateway_get(event, context):
    """
    Get completed data and return it to the caller
    :param event: The HTTP request
    :param context:
    :return:
    """
    data_uuid = event["pathParameters"]["data_uuid"]
    try:
        return s3_client.get_object(Bucket=bucket_name, Key=data_uuid)
    except s3_client.exceptions as e:
        return e


def s3_gateway_post(event, context):
    data_uuid = uuid.uuid4()
    s3 = boto3.resource("s3")
    new_file = s3.Object(f"{data_uuid}.json")
    data = event.get("data")
    response = new_file.put(Body=json.dumps(data).encode("UTF-8"))
    machine = boto3.client("stepfunctions")
    machine.start_execution(
        StateMachineArn=os.environ.get("MATCHING_MACHINE_ARN"),
        name=data_uuid,
        input=json.dumps(
            {
                "matching_function": data.get("matching_function", "quality"),
                "data_uuid": data_uuid,
            }
        ),
    )
    if response:
        return {"status": 201, "uuid": data_uuid}


def s3_gateway_delete(event, context):
    data_uuid = event["pathParameters"]["data_uuid"]
    bucket = boto3.resource("s3").Bucket(bucket_name)
    try:
        bucket.objects.filter(Prefix=data_uuid).delete()
    finally:
        pass
    return {
        "statusCode": 204,
        "headers": {"Content-Type": "application/json"},
        "body": data_uuid,
    }
