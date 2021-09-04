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
    d = path_to_file / "data"
    try:
        d.mkdir()
    except FileExistsError:
        pass
    data_path = d / f"{role_type}.csv"
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


@pytest.fixture
def fifty_random_mentees_and_mentors(tmp_path):
    _random_file(tmp_path, "mentees")
    _random_file(tmp_path, "mentors")


class TestProcess:
    def test_create_mentee_list(self, fifty_random_mentees_and_mentors, tmp_path):
        folder_path = tmp_path / "data"
        mentees = create_participant_list(Mentee, folder_path)
        assert len(mentees) == 50
        assert all(map(lambda role: type(role) is Mentee, mentees))

    def test_create_matches(self, fifty_random_mentees_and_mentors, tmp_path):
        path_to_data = tmp_path / "data"
        matches = create_matches(
            create_participant_list(Mentor, path_to_data),
            create_participant_list(Mentee, path_to_data),
        )
        assert len(matches) == 50
        assert len(matches[0]) == 50

    def test_conduct_matching(self, fifty_random_mentees_and_mentors, tmp_path):
        path_to_data = tmp_path / "data"
        mentors, mentees = conduct_matching(path_to_data)
        assert len(mentors) == 50
        assert len(mentees) == 50
        for mentor in mentors:
            assert len(mentor.mentees) > 0
        for mentee in mentees:
            assert len(mentee.mentors) > 0
