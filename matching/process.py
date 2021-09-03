from match import Match
from munkres import Munkres, make_cost_matrix, Matrix
import sys
from typing import Generator
from mentee import Mentee
from mentor import Mentor


def create_mentee_list() -> Generator[Mentee]:
    pass


def create_mentor_list() -> Generator[Mentor]:
    pass


def create_matches() -> list[list[Match]]:
    return [
        [Match(mentor, mentee) for mentor in create_mentor_list()]
        for mentee in create_mentee_list()
    ]


def prepare_matrix() -> Matrix:
    return make_cost_matrix(
        create_matches(), lambda match: (sys.maxsize - match.quality)
    )


def calculate_matches():
    algorithm = Munkres()
    return algorithm.compute(prepare_matrix())
