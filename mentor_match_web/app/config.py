import os


class Config:
    result_backend = os.environ.get("BACKEND_URL", "BROKEN")
    broker_url = os.environ.get("BROKER_URL", "BROKEN!!")


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    broker_transport_options = {
        "max_retries": 3,
        "interval_start": 0,
        "interval_step": 0.2,
        "interval_max": 0.5,
    }
    broker_url = "redis://localhost:6379/0"
