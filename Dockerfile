FROM python:3.9-slim-bullseye AS parent
MAINTAINER CS LGBTQ+
COPY ./app /app
COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

FROM parent AS web
CMD gunicorn "app:create_app()"

FROM parent AS worker
CMD celery --app=app.extensions.celery worker --loglevel=info
