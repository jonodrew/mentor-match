import os
import time
from matching import process
from typing import Tuple, List
from matching.mentee import Mentee
from matching.mentor import Mentor

from celery import Celery

celery = Celery(
    __name__,
)
celery.conf.broker_url = os.environ.get(
    "CELERY_BROKER_URL", f"{os.environ.get('REDIS_URL')}/0"
)
celery.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", f"{os.environ.get('REDIS_URL')}/0"
)


@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True

@celery.task(name="process_data")
def process_data(data_to_process: Tuple[List[Mentor], List[Mentee]]) -> Tuple[List[Mentor], List[Mentee]]:
    return process.process_data(*data_to_process)
