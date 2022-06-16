import os

from celery import Celery

celery = Celery(
    "app",
    backend=os.environ["REDIS_URL"],
    broker=os.environ["REDIS_URL"],
    include=["app.tasks.tasks"],
    accept_content=["pickle", "json"],
    task_serializer="pickle",
)
