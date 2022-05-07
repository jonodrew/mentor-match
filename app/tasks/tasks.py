import os

import requests
from typing import Tuple, List, Dict
from app.extensions import celery
from matching import process
import matching.rules.rule as rl
import operator
from app.classes import CSParticipantFactory


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
    # hard-code the Rules in here, and work out how to pass them over as JSON/pickle later
    base_rules: List[rl.AbstractRule] = [
        rl.Disqualify(
            lambda match: match.mentee.organisation == match.mentor.organisation
        ),
        rl.Disqualify(rl.Grade(target_diff=2, logical_operator=operator.gt).evaluate),
        rl.Disqualify(rl.Grade(target_diff=0, logical_operator=operator.le).evaluate),
        rl.Grade(1, operator.eq, {True: 3, False: 0}),
        rl.Grade(2, operator.eq, {True: 6, False: 0}),
        rl.Generic(
            {True: 5, False: 0},
            lambda match: match.mentee.target_profession
            == match.mentor.current_profession,
        ),
        rl.Generic(
            {True: 4, False: 0},
            lambda match: match.mentee.characteristic in match.mentor.characteristics,
        ),
    ]
    all_rules = [base_rules for _ in range(3)]
    for i, rules in enumerate(all_rules):
        rules.append(rl.UnmatchedBonus(10**i))
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
