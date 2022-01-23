import time
from typing import Tuple, List
from app.extensions import celery
from matching import process
from matching.factory import ParticipantFactory


@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 9)
    return True


@celery.task(name="async_process_data", bind=True)
def async_process_data(
    self, data_to_process: Tuple[List[dict], List[dict]]
) -> Tuple[List[dict], List[dict]]:
    mentors = [ParticipantFactory.create_from_dict(data) for data in data_to_process[0]]
    mentees = [ParticipantFactory.create_from_dict(data) for data in data_to_process[1]]
    matched_mentors, matched_mentees = process.process_data(mentors, mentees)
    matched_as_dict = [participant.to_dict() for participant in matched_mentors], [
        participant.to_dict() for participant in matched_mentees
    ]
    return matched_as_dict
