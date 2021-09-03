from matching.match import Match
from munkres import Munkres, make_cost_matrix, Matrix
import sys
from typing import Union, Type

from matching.mentee import Mentee
from matching.mentor import Mentor
import csv


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


def prepare_matrix() -> Matrix:
    return make_cost_matrix(
        create_matches(), lambda match: (sys.maxsize - match.quality)
    )


def calculate_matches():
    algorithm = Munkres()
    return algorithm.compute(prepare_matrix())
