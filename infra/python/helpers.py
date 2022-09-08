import json
from typing import Union, TypedDict

from classes import CSMentor, CSMentee, CSParticipantFactory as CSFactory
from tasks import Result


class TaskIO(TypedDict):
    data_uuid: str
    bonus: int


def serialize(
    mentors: list[CSMentor], mentees: list[CSMentee], bonus: int
) -> dict[str, Union[list[dict], int]]:
    return {
        "mentors": [mentor.to_dict() for mentor in mentors],
        "mentees": [mentee.to_dict() for mentee in mentees],
        "unmatched bonus": bonus,
    }


def deserialize(data: dict) -> Result:
    mentors = [
        CSFactory.create_from_dict(mentor_data) for mentor_data in data["mentors"]
    ]
    mentees = [
        CSFactory.create_from_dict(mentee_data) for mentee_data in data["mentees"]
    ]
    unmatched_bonus = data.get("unmatched bonus", 6)
    return [mentors, mentees, unmatched_bonus]


def read_from_s3(event: TaskIO, s3_resource, bucket_name):
    data_uuid = event["data_uuid"]
    step = event.get("bonus", 0)
    data = s3_resource.Object(bucket_name, f"{data_uuid}/{str(step)}.json")
    file_content = data.get()["Body"].read().decode("utf-8")
    return json.loads(file_content)


def write_to_s3(s3_resource, bucket_name, bonus, data_uuid, data_to_write) -> TaskIO:
    data_for_next_step = s3_resource.Object(
        bucket_name, f"{data_uuid}/out/{bonus}.json"
    )
    data_for_next_step.put(Body=(bytes(json.dumps(data_to_write).encode("UTF-8"))))
    return {"data_uuid": data_uuid, "bonus": bonus}
