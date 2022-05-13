import os

import requests
from typing import Tuple, List, Dict
from app.extensions import celery
from matching import process
from app.classes import CSParticipantFactory
from app.helpers import base_rules


@celery.task(name="async_process_data", bind=True)
def async_process_data(
    self,
    data_to_process: Tuple[List[dict], List[dict]],
    weightings_list: List[Dict[str, int]],
) -> Tuple[List[dict], List[dict]]:
    mentors = [
        CSParticipantFactory.create_from_dict(data) for data in data_to_process[0]
    ]
    mentees = [
        CSParticipantFactory.create_from_dict(data) for data in data_to_process[1]
    ]
    all_rules = [base_rules() for _ in range(3)]
    matched_mentors, matched_mentees = process.process_data(
        mentors, mentees, weightings_list, all_rules=all_rules
    )
    matched_as_dict = [participant.to_dict() for participant in matched_mentors], [
        participant.to_dict() for participant in matched_mentees
    ]
    return matched_as_dict


@celery.task(name="delete_mailing_lists_after_period", bind=True)
def delete_mailing_lists_after_period(self, task_id: str):
    url = f"{os.environ.get('SERVICE_URL', 'http://app:5000')}/tasks/{task_id}"
    return requests.delete(url).status_code
