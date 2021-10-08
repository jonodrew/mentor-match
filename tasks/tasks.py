import os
import time
from matching import process
from typing import Tuple, List
from matching.mentee import Mentee
from matching.mentor import Mentor
import asyncio
from extensions import celery


@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 9)
    return True

@celery.task(name="process_data")
def process_data(data_to_process: Tuple[List[Mentor], List[Mentee]]) -> Tuple[List[Mentor], List[Mentee]]:
    return process.process_data(*data_to_process)
