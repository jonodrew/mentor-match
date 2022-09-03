from typing import Union

from classes import CSMentor, CSMentee, CSParticipantFactory as CSFactory
from tasks import Result


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
