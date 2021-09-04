import csv
from typing import Union, Type
from munkres import Munkres, make_cost_matrix, Matrix, DISALLOWED
from matching.match import Match
from matching.mentee import Mentee
from matching.mentor import Mentor
from pathlib import Path


def process_form(path_to_form) -> csv.DictReader:
    with open(path_to_form, "r") as data_form:
        file_reader = csv.DictReader(data_form)
        for row in file_reader:
            yield row


def create_participant_list(
    participant: Union[Type[Mentee], Type[Mentor]], path_to_data
):
    path_to_data = path_to_data / f"{participant.__name__.lower()}s.csv"
    return [participant(**row) for row in process_form(path_to_data)]


def create_matches(
    mentor_list: list[Mentor],
    mentee_list: list[Mentee],
    weightings: Union[None, dict[str, int]] = None,
) -> list[list[Match]]:
    return [
        [Match(mentor, mentee, weightings) for mentor in mentor_list]
        for mentee in mentee_list
    ]


def prepare_matrix(matches: list[list[Match]]) -> Matrix:
    return make_cost_matrix(
        matches,
        lambda match: (DISALLOWED if match.disallowed else match.score),
    )


def calculate_matches(prepared_matrix: Matrix):
    algorithm = Munkres()
    return algorithm.compute(prepared_matrix)


def match_and_assign_participants(
    mentor_list: list[Mentor],
    mentee_list: list[Mentee],
    weightings: Union[dict[str, int], None] = None,
):
    matches = create_matches(mentor_list, mentee_list, weightings)
    for successful_match in calculate_matches(prepare_matrix(matches)):
        match = matches[successful_match[0]][successful_match[1]]
        match.mark_successful()


def round_one_matching(path_to_data) -> tuple[list[Mentor], list[Mentee]]:
    mentors = create_participant_list(Mentor, path_to_data)
    mentees = create_participant_list(Mentee, path_to_data)
    match_and_assign_participants(mentors, mentees)
    return mentors, mentees


def round_two_matching(
    round_one_mentor_list: list[Mentor], round_one_mentee_list: list[Mentee]
) -> tuple[list[Mentor], list[Mentee]]:
    match_and_assign_participants(
        round_one_mentor_list,
        round_one_mentee_list,
        weightings={"profession": 4, "grade": 3, "unmatched bonus": 1.5},
    )
    return round_one_mentor_list, round_one_mentee_list


def round_three_matching(
    round_two_mentor_list: list[Mentor], round_two_mentee_list: list[Mentee]
) -> tuple[list[Mentor], list[Mentee]]:
    match_and_assign_participants(
        round_two_mentor_list,
        round_two_mentee_list,
        weightings={"profession": 0, "grade": 3, "unmatched bonus": 2},
    )
    return round_two_mentor_list, round_two_mentee_list


def conduct_matching(path_to_data):
    return round_three_matching(*round_two_matching(*round_one_matching(path_to_data)))


def create_mailing_list(
    participant_list: list[Union[Mentor, Mentee]], output_folder: Path
):
    file_name = f"{type(participant_list[0]).__name__.lower()}s-list.csv"
    file = output_folder.joinpath(file_name)
    participant_list = [participant.to_dict() for participant in participant_list]
    with open(file, "w", newline="") as output_file:
        field_headings = list(participant_list[0].keys())
        writer = csv.DictWriter(output_file, fieldnames=field_headings)
        writer.writeheader()
        for participant in participant_list:
            writer.writerow(participant)
