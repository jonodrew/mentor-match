import os
import sys
import requests
from typing import Tuple, List, Sequence

from app.classes import CSMentor, CSMentee
from app.extensions import celery_app as celery_app
from matching import process
from app.helpers import base_rules
from matching.rules.rule import UnmatchedBonus

sys.setrecursionlimit(10000)


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


@celery_app.task
def find_best_output(
    group_result: Sequence[tuple[list[CSMentor], list[CSMentee], int]]
) -> tuple[list[CSMentor], list[CSMentee]]:
    highest_count_mentees_with_mentor = 0
    best_outcome = None
    unmatched_bonus = sys.maxsize
    for participant_tuple in group_result:
        count_mentees_with_at_least_one_mentor = sum(
            map(lambda mentee: len(mentee.mentors) > 0, participant_tuple[1])
        )
        if (
            count_mentees_with_at_least_one_mentor > highest_count_mentees_with_mentor
            and participant_tuple[2] <= unmatched_bonus
        ):
            best_outcome = participant_tuple[:2]
            highest_count_mentees_with_mentor = count_mentees_with_at_least_one_mentor
            unmatched_bonus = participant_tuple[2]
    if not best_outcome:
        best_outcome = group_result[0][:2]
    return best_outcome


@celery_app.task(name="delete_mailing_lists_after_period", bind=True)
def delete_mailing_lists_after_period(self, task_id: str):
    url = f"{os.environ.get('SERVICE_URL', 'http://app:5000')}/tasks/{task_id}"
    return requests.delete(url).status_code
