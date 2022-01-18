FROM python:3.9-slim-bullseye
MAINTAINER CS LGBTQ+
COPY ./app /app
COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt
