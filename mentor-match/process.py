from match import Match
from munkres import Munkres, make_cost_matrix, print_matrix
import sys

def create_mentee_list():
    pass

def create_mentor_list():
    pass

def create_matches() -> list[list[Match]]:
    return [[Match(mentor, mentee) for mentor in create_mentor_list()] for mentee in create_mentee_list()]

def prepare_matrix():
    return make_cost_matrix(create_matches(), lambda match: (sys.maxsize-match.quality))

def calculate_matches():
    algorithm = Munkres()
    matrix = create_matches()
    indexes = algorithm.compute(prepare_matrix())
    print_matrix(matrix, msg='Highest profit through this matrix:')
    total = 0
    for row, column in indexes:
        successful_match = matrix[row][column]
        total += successful_match.score
        print(f'({successful_match.mentee.name}, {successful_match.mentor.name}) -> {successful_match.score}')
    print(f'total profit={total}')