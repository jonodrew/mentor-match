import os


class Config:
    CELERY_RESULT_BACKEND = os.environ.get("REDIS_URL", "BROKEN")
    CELERY_BROKER_URL = os.environ.get("REDIS_URL", "BROKEN!!")


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    BROKER_TRANSPORT_OPTIONS = {
        "max_retries": 3,
        "interval_start": 0,
        "interval_step": 0.2,
        "interval_max": 0.5,
    }
    os.environ["REDIS_URL"] = "redis@redis"
