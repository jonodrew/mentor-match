FROM python:3.9-slim-bullseye AS parent
MAINTAINER CS LGBTQ+
COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt
COPY ./app /app

FROM parent AS web
CMD ["gunicorn", "app:create_app()"]

FROM parent AS worker
CMD celery --app=app.extensions.celery_app worker --loglevel=info
