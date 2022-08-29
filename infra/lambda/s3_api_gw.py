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
    data_uuid = event["uuid"]
    try:
        return s3_client.get_object(Bucket=bucket_name, Key=data_uuid)
    except s3_client.exceptions as e:
        return e


def s3_gateway_post(event, context):
    data_uuid = uuid.uuid4()
    response = s3_client.put_object(
        Bucket=bucket_name, Key=data_uuid, Body=event.get("data")
    )
    if response:
        return {"status": 201, "uuid": data_uuid}


def s3_gateway_delete(event, context):
    bucket = boto3.resource("s3").Bucket(bucket_name)
    data_uuid = event["uuid"]
    bucket.objects.filter(Prefix=data_uuid).delete()
    return {
        "statusCode": 204,
        "headers": {"Content-Type": "application/json"},
        "body": data_uuid,
    }
