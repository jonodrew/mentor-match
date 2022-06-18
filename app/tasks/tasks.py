import os
from copy import deepcopy
import celery
import requests
from typing import Tuple, List, Sequence

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
) -> Tuple[List[CSMentor], List[CSMentee], int]:
    all_rules = [base_rules() for _ in range(3)]
    for ruleset in all_rules:
        ruleset.append(UnmatchedBonus(unmatched_bonus))
    matched_mentors, matched_mentees = process.process_data(
        list(mentors), list(mentees), all_rules=all_rules
    )
    return matched_mentors, matched_mentees, unmatched_bonus


@celery_app.task(bind=True)
def process_data_with_floor(
    self, mentors: list[CSMentor], mentees: list[CSMentee], floor=0.7
):
    max_score = sum(rule.results.get(True) for rule in base_rules())
    all_permutations = celery.chord(
        (
            async_process_data.s(deepcopy(mentors), deepcopy(mentees), i)
            for i in range(max_score)
        ),
        find_best_output.s(),
    )
    return all_permutations()


@celery_app.task
def find_best_output(group_result: Sequence[tuple[list[CSMentor], list[CSMentee]]]):
    highest = 0
    best_outcome = None
    for participant_tuple in group_result:
        total_mentors = sum(
            map(lambda mentee: len(mentee.mentors), participant_tuple[1])
        )
        if total_mentors > highest:
            best_outcome = participant_tuple
            highest = total_mentors
    if not best_outcome:
        best_outcome = group_result[0][:2]
    return best_outcome


@celery_app.task(name="delete_mailing_lists_after_period", bind=True)
def delete_mailing_lists_after_period(self, task_id: str):
    url = f"{os.environ.get('SERVICE_URL', 'http://app:5000')}/tasks/{task_id}"
    return requests.delete(url).status_code
