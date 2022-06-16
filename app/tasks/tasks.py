import os

import celery
import requests
from typing import Tuple, List
from app.extensions import celery as celery_app
from matching import process
from app.helpers import base_rules
from matching.rules.rule import UnmatchedBonus


@celery.shared_task
@celery_app.task(name="async_process_data", bind=True, serializer="pickle")
def async_process_data(
    self,
    mentors,
    mentees,
    unmatched_bonus: int = 6,
) -> Tuple[List[dict], List[dict]]:
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


@celery_app.task(name="delete_mailing_lists_after_period", bind=True)
def delete_mailing_lists_after_period(self, task_id: str):
    url = f"{os.environ.get('SERVICE_URL', 'http://app:5000')}/tasks/{task_id}"
    return requests.delete(url).status_code
