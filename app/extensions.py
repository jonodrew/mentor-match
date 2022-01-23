from celery import Celery

celery = Celery(include=['app.tasks.tasks'])
