import pytest as pytest

from matching.mentee import Mentee
from matching.mentor import Mentor


@pytest.fixture
def base_data() -> dict:
    return {
        "Your first name": "Test",
        "Your last name": "Data",
        "Your Civil Service email address": "test@data.com",
        "Your job title or role": "N/A",
        "Your department or agency": "Department of Fun",
        "Your grade": "Grade 7",
        "Your profession": "Policy",
    }


@pytest.fixture
def base_mentee(base_data):
    return Mentee(**base_data)


@pytest.fixture
def base_mentor(base_data):
    data_copy = base_data.copy()
    data_copy["Your grade"] = "Grade 6"
    data_copy["Your department or agency"] = "Ministry of Silly Walks"
    return Mentor(**data_copy)
