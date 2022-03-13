import os

import requests
from typing import Tuple, List, Dict
from app.extensions import celery
from matching import process
from matching.factory import ParticipantFactory


@celery.task(name="async_process_data", bind=True)
def async_process_data(
    self,
    data_to_process: Tuple[List[dict], List[dict]],
    weightings_list: List[Dict[str, int]],
) -> Tuple[List[dict], List[dict]]:
    mentors = [ParticipantFactory.create_from_dict(data) for data in data_to_process[0]]
    mentees = [ParticipantFactory.create_from_dict(data) for data in data_to_process[1]]
    matched_mentors, matched_mentees = process.process_data(
        mentors, mentees, weightings_list
    )
    matched_as_dict = [participant.to_dict() for participant in matched_mentors], [
        participant.to_dict() for participant in matched_mentees
    ]
    return matched_as_dict


@celery.task(name="delete_mailing_lists_after_period", bind=True)
def delete_mailing_lists_after_period(self, task_id: str):
    url = f"{os.environ.get('SERVICE_URL', 'http://app:5000')}/tasks/{task_id}"
    return requests.delete(url).status_code
