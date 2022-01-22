import os


class Config:
    CELERY_RESULT_BACKEND = os.environ.get(
        "CELERY_BROKER_URL", f"{os.environ.get('REDIS_URL')}/0"
    )
    CELERY_BROKER_URL = os.environ.get(
        "CELERY_RESULT_BACKEND", f"{os.environ.get('REDIS_URL')}/0"
    )


class TestConfig(Config):
    ENV = "test"
    DEBUG = True
    CELERY_RESULT_BACKEND = "rpc://"
    CELERY_BROKER_URL = "amqp://myuser:mypassword@localhost/myvhost"
    BROKER_TRANSPORT_OPTIONS = {
        "max_retries": 3,
        "interval_start": 0,
        "interval_step": 0.2,
        "interval_max": 0.5,
    }
