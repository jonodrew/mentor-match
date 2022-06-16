import os


class Config:
    result_backend = os.environ.get("REDIS_URL", "BROKEN")
    broker_url = os.environ.get("REDIS_URL", "BROKEN!!")


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    broker_transport_options = {
        "max_retries": 3,
        "interval_start": 0,
        "interval_step": 0.2,
        "interval_max": 0.5,
    }
    if os.environ.get("REDIS_URL") is None:
        os.environ["REDIS_URL"] = "redis@redis"
