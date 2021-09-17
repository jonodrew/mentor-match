import csv
import logging
import os
import sys
from pathlib import Path
from typing import Union, Type, List, Dict, Tuple, Generator, Optional

from munkres import Munkres, make_cost_matrix, Matrix  # type: ignore

from matching.helpers.pre_processing import transpose_matrix
from matching.match import Match
from matching.mentee import Mentee
from matching.mentor import Mentor


def generate_match_matrix(
    mentor_list: List[Mentor],
    mentee_list: List[Mentee],
    weightings: Optional[Dict[str, int]],
) -> List[List[Match]]:
    return [
        [Match(mentor, mentee, weightings) for mentee in mentee_list]
        for mentor in mentor_list
    ]


def process_form(path_to_form) -> Generator[Dict[str, str], None, None]:
    with open(path_to_form, "r") as data_form:
        file_reader = csv.DictReader(data_form)
        for row in file_reader:
            yield row


def create_participant_list(
    participant: Union[Type[Mentee], Type[Mentor]], path_to_data
):
    path_to_data = path_to_data / f"{participant.__name__.lower()}s.csv"
    return [participant(**row) for row in process_form(path_to_data)]


def _mark_participants_with_no_matches(matrix: List[List[Match]], role_as_str: str):
    for row in matrix:
        if all([match.disallowed for match in row]):
            row[0].__getattribute__(role_as_str).has_no_match = True
            logging.debug(
                f"Participant {row[0].__getattribute__(role_as_str).data['Your Civil Service email address']} has no matches"
            )


def create_matches(
    mentor_list: List[Mentor],
    mentee_list: List[Mentee],
    weightings: Union[None, Dict[str, int]] = None,
) -> List[List[Match]]:
    def _can_match(participant: Union[Mentor, Mentee]):
        return not participant.has_no_match

    preliminary_matches = generate_match_matrix(mentor_list, mentee_list, weightings)
    _mark_participants_with_no_matches(preliminary_matches, "mentor")
    _mark_participants_with_no_matches(transpose_matrix(preliminary_matches), "mentee")
    return generate_match_matrix(
        list(filter(_can_match, mentor_list)),
        list(filter(_can_match, mentee_list)),
        weightings,
    )


def prepare_matrix(matches: List[List[Match]]) -> Matrix:
    prepared_matrix = make_cost_matrix(
        matches,
        lambda match: sys.maxsize - match.score,
    )
    return prepared_matrix


def calculate_matches(prepared_matrix: Matrix):
    algorithm = Munkres()
    return algorithm.compute(prepared_matrix)


def match_and_assign_participants(
    mentor_list: List[Mentor],
    mentee_list: List[Mentee],
    weightings: Union[Dict[str, int], None] = None,
):
    matches = create_matches(mentor_list, mentee_list, weightings)
    for successful_match in calculate_matches(prepare_matrix(matches)):
        match = matches[successful_match[0]][successful_match[1]]
        match.mark_successful()


def round_one_matching(path_to_data) -> Tuple[List[Mentor], List[Mentee]]:
    mentors = create_participant_list(Mentor, path_to_data)
    mentees = create_participant_list(Mentee, path_to_data)
    match_and_assign_participants(mentors, mentees)
    return mentors, mentees


def round_two_matching(
    round_one_mentor_list: List[Mentor], round_one_mentee_list: List[Mentee]
) -> Tuple[List[Mentor], List[Mentee]]:
    logging.debug("Round two!")
    match_and_assign_participants(
        round_one_mentor_list,
        round_one_mentee_list,
        weightings={"profession": 4, "grade": 3, "unmatched bonus": 50},
    )
    return round_one_mentor_list, round_one_mentee_list


def round_three_matching(
    round_two_mentor_list: List[Mentor], round_two_mentee_list: List[Mentee]
) -> Tuple[List[Mentor], List[Mentee]]:
    match_and_assign_participants(
        round_two_mentor_list,
        round_two_mentee_list,
        weightings={"profession": 0, "grade": 3, "unmatched bonus": 100},
    )
    return round_two_mentor_list, round_two_mentee_list


def conduct_matching(path_to_data):
    return round_three_matching(*round_two_matching(*round_one_matching(path_to_data)))


def create_mailing_list(
    participant_list: List[Union[Mentor, Mentee]], output_folder: Path
):
    file_name = f"{type(participant_list[0]).__name__.lower()}s-list.csv"
    file = output_folder.joinpath(file_name)
    list_participants_as_dicts = [
        participant.to_dict() for participant in participant_list
    ]
    field_headings = list_participants_as_dicts[0].keys()
    length_headings = len(field_headings)
    for participant in list_participants_as_dicts:
        if len(participant.keys()) > length_headings:
            field_headings = participant.keys()
    try:
        os.mkdir(output_folder)
    except FileExistsError:
        pass
    with open(file, "w", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=list(field_headings))
        writer.writeheader()
        for participant in list_participants_as_dicts:
            writer.writerow(participant)
