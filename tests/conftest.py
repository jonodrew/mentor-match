import csv
import math
import pathlib
from datetime import datetime
import pytest as pytest

import app.helpers
from app import create_app
from app.config import TestConfig
from matching.mentee import Mentee
from matching.mentor import Mentor
from matching.process import create_participant_list_from_path


@pytest.fixture(scope="session")
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


@pytest.fixture(scope="session")
def base_mentee(base_data):
    return Mentee(**base_data)


@pytest.fixture(scope="session")
def base_mentor(base_data):
    data_copy = base_data.copy()
    data_copy["Your grade"] = "Grade 6"
    data_copy["Your department or agency"] = "Ministry of Silly Walks"
    return Mentor(**data_copy)


@pytest.fixture(scope="session")
def known_file(base_data):
    def _known_file(path_to_file, role_type: str, quantity=50):
        padding_size = int(math.log10(quantity)) + 1
        pathlib.Path(path_to_file).mkdir(parents=True, exist_ok=True)
        data_path = path_to_file / f"{role_type}s.csv"
        with open(data_path, "w", newline="") as test_data:
            headings = [
                "Timestamp",
                f"Do you want to sign up as a {role_type}?",
                "Do you agree to us using the information you provide to us in this way?",
                "Your first name",
                "Your last name",
                "Your Civil Service email address",
                "Your job title or role",
                "Your department or agency",
                "Your grade",
                "Your profession",
            ]
            data = [headings]
            for i in range(quantity):
                data.append(
                    [
                        str(datetime.now()),
                        "yes",
                        "yes",
                        role_type,
                        str(i).zfill(padding_size),
                        f"{role_type}.{str(i).zfill(padding_size)}@gov.uk",
                        "Some role",
                        f"Department of {role_type.capitalize()}s",
                        "EO" if role_type == "mentor" else "AA",
                        "Participant",
                    ]
                )
            file_writer = csv.writer(test_data)
            file_writer.writerows(data)

    return _known_file


@pytest.fixture(scope="session")
def test_data_path(tmpdir_factory):
    return tmpdir_factory.mktemp("data")


@pytest.fixture
def client(test_data_path):
    test_app = create_app(TestConfig)
    test_app.config["UPLOAD_FOLDER"] = test_data_path
    with test_app.test_client() as client:
        yield client


@pytest.fixture(scope="session")
def test_participants(test_data_path, known_file):
    known_file(test_data_path, "mentee", 50)
    known_file(test_data_path, "mentor", 50)
    create_participant_list_from_path(Mentee, test_data_path)
    create_participant_list_from_path(Mentor, test_data_path)
    yield


@pytest.fixture(autouse=True)
def predictable_random_string(monkeypatch):
    def predictable_string():
        return "abcdef"

    monkeypatch.setattr(app.helpers, "random_string", predictable_string)
