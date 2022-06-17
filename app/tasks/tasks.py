import os
from copy import deepcopy
import celery
import requests
from typing import Tuple, List

from app.classes import CSMentor, CSMentee
from app.extensions import celery_app as celery_app
from matching import process
from app.helpers import base_rules
from matching.rules.rule import UnmatchedBonus


@celery_app.task(name="async_process_data", bind=True)
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
    return matched_mentors, matched_mentees


@celery.shared_task
@celery_app.task
def process_data_with_floor(
    mentors: list[CSMentor], mentees: list[CSMentee], floor=0.7
):
    max_score = sum(rule.results.get(True) for rule in base_rules())
    return celery.group(
        async_process_data.s(deepcopy(mentors), deepcopy(mentees), i)
        for i in range(max_score)
    )()


@celery_app.task
def find_best_output(group_result):
    pass


@celery_app.task(name="delete_mailing_lists_after_period", bind=True)
def delete_mailing_lists_after_period(self, task_id: str):
    url = f"{os.environ.get('SERVICE_URL', 'http://app:5000')}/tasks/{task_id}"
    return requests.delete(url).status_code
