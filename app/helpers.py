import string
import random
from typing import Union


def valid_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() == "csv"


def mentors_and_mentees_present(filenames: list[str]) -> bool:
    """
    This function picks off the string after the last forward slash in each filename and then checks that they are
    'mentors.csv' and 'mentees.csv'
    :param filenames:
    :return:
    """
    return set(
        map(lambda filename: filename.rsplit("/", 1)[-1].lower(), filenames)
    ) == {
        "mentors.csv",
        "mentees.csv",
    }


def valid_files(filenames: list[str]) -> bool:
    return mentors_and_mentees_present(filenames) and all(map(valid_file, filenames))


def random_string():
    return "".join(random.choice(string.ascii_lowercase) for _ in range(10))


def form_to_library_mapping(
    form_dict: dict[str, str], participant_type: str
) -> dict[str, Union[str, int]]:
    mapping = {
        f"Do you want to sign up as a {participant_type}?": participant_type,
        "Your first name": "first name",
        "Your last name": "last name",
        "Your Civil Service email address": "email",
        "Your job title or role": "role",
        "Your department or agency": "organisation",
        "Your grade": "grade",
        "Your profession": "current profession",
    }
    new_dict: dict[str, Union[str, int]] = {}
    for key, value in form_dict.items():
        if key in mapping:
            if key == "Your grade":
                new_dict[mapping[key]] = convert_grade_to_int(value)
            else:
                new_dict[mapping[key]] = value
        else:
            new_dict[key] = value
    return new_dict


def convert_grade_to_int(grade: str) -> int:
    grades = [
        "AA",
        "AO",
        "EO",
        "HEO",
        "SEO",
        "Grade 7",
        "Grade 6",
        "SCS1",
        "SCS2",
        "SCS3",
        "SCS4",
    ]
    return grades.index(grade)
