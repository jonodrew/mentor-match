import csv
import logging
import math
import os
import pathlib
from datetime import datetime
from typing import List

import pytest

from matching.mentor import Mentor
from matching.person import Person
from matching.process import (
    create_participant_list,
    Mentee,
    create_matches,
    conduct_matching,
    create_mailing_list,
)


@pytest.fixture
def known_file(base_data):
    def known_file(path_to_file, role_type: str, quantity=50):
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

    return known_file


@pytest.fixture(scope="session")
def test_data_path(tmpdir_factory):
    return tmpdir_factory.mktemp("data")


class TestProcess:
    def test_create_mentee_list(self, known_file, test_data_path):
        known_file(test_data_path, "mentee", 50)
        mentees = create_participant_list(Mentee, test_data_path)
        assert len(mentees) == 50
        assert all(map(lambda role: type(role) is Mentee, mentees))

    def test_create_matches(self, known_file, test_data_path):
        known_file(test_data_path, "mentee", 50)
        known_file(test_data_path, "mentor", 50)
        matches = create_matches(
            create_participant_list(Mentor, test_data_path),
            create_participant_list(Mentee, test_data_path),
        )
        assert len(matches) == 50
        assert len(matches[0]) == 50

    def test_conduct_matching(self, known_file, test_data_path):
        known_file(test_data_path, "mentee", 50)
        known_file(test_data_path, "mentor", 50)
        mentors, mentees = conduct_matching(test_data_path)
        assert len(mentors) == 50
        assert len(mentees) == 50
        for mentor in mentors:
            assert len(mentor.mentees) > 0
        for mentee in mentees:
            assert len(mentee.mentors) > 0

    def test_conduct_matching_with_unbalanced_inputs(self, test_data_path, known_file):
        known_file(test_data_path, "mentee", 50)
        known_file(test_data_path, "mentor", 35)
        mentors, mentees = conduct_matching(test_data_path)
        every_mentee_has_a_mentor = list(
            map(lambda mentee: len(mentee.mentors) > 0, mentees)
        )
        logging.debug(
            f"Mentees without a mentor: {every_mentee_has_a_mentor.count(False)}"
        )
        assert all(every_mentee_has_a_mentor)

    @pytest.mark.skipif(
        os.environ.get("TEST") is None, reason="can't put integration data on Github"
    )
    def test_integration_data(self):
        def _unmatchables(list_participants: List[Person]):
            return len(
                [
                    participant
                    for participant in list_participants
                    if participant.has_no_match and len(participant.connections) == 0
                ]
            )

        mentors, mentees = conduct_matching(
            pathlib.Path(".").absolute() / "integration"
        )
        every_mentee_has_a_mentor = list(
            map(lambda mentee: len(mentee.mentors) > 0, mentees)
        )
        logging.info(
            f"Mentees without a mentor: {every_mentee_has_a_mentor.count(False)}\n"
            f"Mentors without any mentees {list(map(lambda mentor: len(mentor.mentees) > 0, mentors)).count(False)}"
        )
        logging.info(
            f"Total matches made: {sum(map(lambda participant: len(participant.connections), mentees))}"
        )
        logging.info(
            f"Unmatchable mentors: {_unmatchables(mentors)} | mentees: {_unmatchables(mentees)}"
        )
        assert all(every_mentee_has_a_mentor)

    def test_create_mailing_list(self, tmp_path, base_mentee, base_mentor, base_data):
        mentors = [base_mentor]
        for mentor in mentors:
            mentor.mentees.extend([base_mentee for _ in range(3)])
        create_mailing_list(mentors, tmp_path)
        assert tmp_path.joinpath("mentors-list.csv").exists()
        with open(tmp_path.joinpath("mentors-list.csv"), "r") as test_mentors_file:
            file_reader = csv.reader(test_mentors_file)
            assert {"match 1 email", "match 2 email", "match 3 email"}.issubset(
                set(next(file_reader))
            )
