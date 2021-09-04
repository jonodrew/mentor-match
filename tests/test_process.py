import csv
import math
import random
import string
from datetime import datetime

import pytest

from matching.mentor import Mentor
from matching.person import GRADES, ORGS, PROFESSIONS
from matching.process import (
    create_participant_list,
    Mentee,
    create_matches,
    conduct_matching,
)


def _random_file(path_to_file, role_type: str, quantity=50):
    padding_size = int(math.log10(quantity)) + 1
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
                    datetime.now(),
                    "yes",
                    "yes",
                    role_type,
                    str(i).zfill(padding_size),
                    "".join(random.choices(string.ascii_letters + string.digits, k=16)),
                    "".join(random.choices(string.ascii_letters + string.digits, k=16)),
                    random.choice(ORGS),
                    random.choice(GRADES),
                    random.choice(PROFESSIONS),
                ]
            )
        file_writer = csv.writer(test_data)
        file_writer.writerows(data)


@pytest.fixture(scope="session")
def test_data_path(tmpdir_factory):
    return tmpdir_factory.mktemp("data")


@pytest.fixture(scope="session")
def fifty_random_mentees_and_mentors(test_data_path):
    _random_file(test_data_path, "mentee")
    _random_file(test_data_path, "mentor")


class TestProcess:
    def test_create_mentee_list(self, fifty_random_mentees_and_mentors, test_data_path):
        mentees = create_participant_list(Mentee, test_data_path)
        assert len(mentees) == 50
        assert all(map(lambda role: type(role) is Mentee, mentees))

    def test_create_matches(self, fifty_random_mentees_and_mentors, test_data_path):
        matches = create_matches(
            create_participant_list(Mentor, test_data_path),
            create_participant_list(Mentee, test_data_path),
        )
        assert len(matches) == 50
        assert len(matches[0]) == 50

    def test_conduct_matching(self, fifty_random_mentees_and_mentors, test_data_path):
        mentors, mentees = conduct_matching(test_data_path)
        assert len(mentors) == 50
        assert len(mentees) == 50
        for mentor in mentors:
            assert len(mentor.mentees) > 0
        for mentee in mentees:
            assert len(mentee.mentors) > 0

    def test_deserialise_participant_to_csv(self, test_data_path):
        pass
