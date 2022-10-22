from copy import deepcopy

import celery
from celery.result import AsyncResult

from app.classes import CSMentor, CSMentee
from app.helpers import base_rules
from app.tasks.tasks import async_process_data, find_best_output


def most_mentees_with_at_least_one_mentor(
    mentors: list[CSMentor], mentees: list[CSMentee]
) -> AsyncResult:
    max_score = sum(rule.results.get(True) for rule in base_rules())
    copies = ((deepcopy(mentors), deepcopy(mentees), i) for i in range(max_score))
    task = celery.chord(
        (async_process_data.si(*data) for data in copies), find_best_output.s()
    )()
    return task
