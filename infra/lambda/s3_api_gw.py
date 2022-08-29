import uuid

import os

import boto3
from aws_cdk.aws_ses_actions import S3

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
    except S3.Client.exceptions as e:
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
