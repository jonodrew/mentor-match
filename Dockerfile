FROM python:3.9-slim-bullseye
MAINTAINER CS LGBTQ+
COPY ./app /app
COPY ./client_secret_655796018812-7t5put9apqg7sas5j6c0e9bgcc224lem.apps.googleusercontent.com.json /client_secret_655796018812-7t5put9apqg7sas5j6c0e9bgcc224lem.apps.googleusercontent.com.json
COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt
