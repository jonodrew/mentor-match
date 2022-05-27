import os

import requests
from typing import Tuple, List
from app.extensions import celery
from matching import process
from app.classes import CSParticipantFactory
from app.helpers import base_rules
from matching.rules.rule import UnmatchedBonus


@celery.task(name="async_process_data", bind=True)
def async_process_data(
    self,
    mentor_data,
    mentee_data,
    unmatched_bonus: int = 6,
) -> Tuple[List[dict], List[dict]]:
    mentors = map(CSParticipantFactory.create_from_dict, mentor_data)
    mentees = map(CSParticipantFactory.create_from_dict, mentee_data)
    all_rules = [base_rules() for _ in range(3)]
    for ruleset in all_rules:
        ruleset.append(UnmatchedBonus(unmatched_bonus))
    matched_mentors, matched_mentees = process.process_data(
        list(mentors), list(mentees), all_rules=all_rules
    )
    matched_as_dict = [participant.to_dict() for participant in matched_mentors], [
        participant.to_dict() for participant in matched_mentees
    ]
    return matched_as_dict


@celery.task(name="delete_mailing_lists_after_period", bind=True)
def delete_mailing_lists_after_period(self, task_id: str):
    url = f"{os.environ.get('SERVICE_URL', 'http://app:5000')}/tasks/{task_id}"
    return requests.delete(url).status_code
