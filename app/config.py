import os


class Config:
    CELERY_RESULT_BACKEND = os.environ.get(
        "REDIS_URL", os.environ.get("CELERY_RESULT_BACKEND")
    )
    CELERY_BROKER_URL = os.environ.get("REDIS_URL", os.environ.get("CELERY_BROKER_URL"))


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    CELERY_RESULT_BACKEND = "rpc://"
    CELERY_BROKER_URL = "amqp://myuser:mypassword@localhost/myvhost"
    BROKER_TRANSPORT_OPTIONS = {
        "max_retries": 3,
        "interval_start": 0,
        "interval_step": 0.2,
        "interval_max": 0.5,
    }
