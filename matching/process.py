import csv
from typing import Union, Type

from munkres import Munkres, make_cost_matrix, Matrix, DISALLOWED

from matching.match import Match
from matching.mentee import Mentee
from matching.mentor import Mentor


def process_form(path_to_form) -> csv.DictReader:
    with open(path_to_form, "r") as data_form:
        file_reader = csv.DictReader(data_form)
        for row in file_reader:
            yield row


def create_participant_list(
    participant: Union[Type[Mentee], Type[Mentor]], path_to_data
):
    return [participant(**row) for row in process_form(path_to_data)]


def create_matches(path_to_data) -> list[list[Match]]:
    return [
        [
            Match(mentor, mentee)
            for mentor in create_participant_list(Mentor, path_to_data / "mentors.csv")
        ]
        for mentee in create_participant_list(Mentee, path_to_data / "mentees.csv")
    ]


def prepare_matrix(path_to_data) -> Matrix:
    return make_cost_matrix(
        create_matches(path_to_data),
        lambda match: (DISALLOWED if match.disallowed else match.score),
    )


def calculate_matches(path_to_data):
    algorithm = Munkres()
    return algorithm.compute(prepare_matrix(path_to_data))
