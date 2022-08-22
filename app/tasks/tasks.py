import functools
import os
import sys
import requests
from typing import Tuple, List, Sequence, Protocol

from app.classes import CSMentor, CSMentee
from app.extensions import celery_app as celery_app
from matching import process
from app.helpers import base_rules
from matching.rules.rule import UnmatchedBonus

sys.setrecursionlimit(10000)


class Exporter(Protocol):
    def send_email(self, recipient: str, **kwargs):
        ...


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
) -> tuple[list[CSMentor], list[CSMentee], int]:
    """
    This function gathers all the outcomes together and finds the best. The best is defined as the outcome where the
    most mentees have at least one mentor, and the most possible mentors have at least one mentee
    """
    highest_count = {"mentors": 0, "mentees": 0}
    best_outcome = group_result[0]
    for participant_tuple in group_result:
        mentors, mentees, unmatched_bonus = participant_tuple
        one_connection_min_func = functools.partial(
            map, lambda participant: len(participant.connections) > 0
        )
        current_count = {
            "mentors": sum(one_connection_min_func(mentors)),
            "mentees": sum(one_connection_min_func(mentees)),
        }
        if (current_count["mentees"] > highest_count["mentees"]) or (  # type: ignore
            current_count["mentees"] == highest_count["mentees"]
            and current_count["mentors"] > highest_count["mentors"]  # type: ignore
        ):  # type: ignore
            best_outcome = participant_tuple
            highest_count = current_count  # type: ignore
    return best_outcome


@celery_app.task(name="delete_mailing_lists_after_period", bind=True)
def delete_mailing_lists_after_period(self, task_id: str):
    url = f"{os.environ.get('SERVICE_URL', 'http://app:5000')}/tasks/{task_id}"
    return requests.delete(url).status_code


@celery_app.task
def send_notification(exporter: Exporter, participant_data: dict[str, str]):
    return exporter.send_email(
        participant_data.get("email address", ""), **participant_data
    )
