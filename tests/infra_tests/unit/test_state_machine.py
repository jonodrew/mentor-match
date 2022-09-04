import json
import os

import boto3
from moto import mock_s3
import pytest

test_bucket = "testing-bucket"
data_uuid = "test_data_uuid"


@pytest.fixture
def s3_resource(aws_credentials):
    with mock_s3():
        yield boto3.resource('s3')


@pytest.fixture
def setup_data(s3_resource, participants_as_json):
    # We need to create the bucket since this is all in Moto's 'virtual' AWS account
    s3_resource.create_bucket(Bucket=test_bucket)
    s3_resource.Object(test_bucket, f"{data_uuid}/0.json").put(Body=(bytes(participants_as_json.encode("UTF-8"))))
    yield


@pytest.fixture
def quantity_flow():
    ...


@pytest.fixture
def quality_flow():
    ...


@pytest.fixture
def participants_as_json(known_participants):
    participants = known_participants()
    return json.dumps(
        {"mentors": [p.to_dict() for p in participants[0]],
         "mentees": [p.to_dict() for p in participants[1]],
         "unmatched bonus": 6})


@pytest.fixture(scope="function", autouse=True)
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
    os.environ["S3_BUCKET_NAME"] = test_bucket


@pytest.mark.unit
def test_state_machine_quality(participants_as_json, setup_data, s3_resource):
    """
    This tests the state machine flow for a simple case
    :return:
    """
    from infra.app.index import async_process_data_event_handler
    output = async_process_data_event_handler({"data_uuid": data_uuid, "step": 0}, None)
    assert output == {"data_uuid": data_uuid, "step": 1}
    assert s3_resource.Object(test_bucket, f"{data_uuid}/{str(output['step'])}.json")


@pytest.mark.integration
def test_state_machine_quantity(participants_as_json, setup_data, s3_resource):
    from infra.app.index import prepare_data_for_mapping, async_process_data_event_handler, find_best_result_lambda
    step_one = prepare_data_for_mapping({"data_uuid": data_uuid, "step": 0}, None)
    iterator = s3_resource.Object(test_bucket, f"{data_uuid}/{str(step_one['step'])}.json")
