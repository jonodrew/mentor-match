import os

from celery import Celery

celery_app = Celery(
    "celery_app",
    backend=os.environ["BACKEND_URL"],
    broker=os.environ["BROKER_URL"],
    include=["app.tasks.tasks"],
    accept_content=["pickle", "json"],
    task_serializer="pickle",
    result_serializer="pickle",
)
