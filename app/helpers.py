import csv
import math
import operator
import pathlib
import string
import random
import matching.rules.rule as rl


def grades() -> list[str]:
    return [
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


def known_file(path_to_file, role_type: str, quantity=50):
    padding_size = int(math.log10(quantity)) + 1
    pathlib.Path(path_to_file).mkdir(parents=True, exist_ok=True)
    data_path = path_to_file / f"{role_type}s.csv"
    with open(data_path, "w", newline="") as test_data:
        data = known_data(role_type)
        file_writer: csv.DictWriter[str] = csv.DictWriter(test_data, list(data.keys()))
        rows = []
        for i in range(quantity):
            data["last name"] = str(i).zfill(padding_size)
            data["email address"] = f"{role_type}.{str(i).zfill(padding_size)}@gov.uk"
            rows.append(data.copy())
        file_writer.writeheader()
        file_writer.writerows(rows)


def known_data(role_type: str):
    data = {
        "first name": role_type,
        "last name": "",
        "email address": "",
        "both mentor and mentee": "no",
        "job title": "Some role",
        "grade": "EO" if role_type == "mentor" else "AA",
        "organisation": f"Department of {role_type.capitalize()}s",
        "biography": "Test biography",
    }
    if role_type == "mentor":
        data["profession"] = "Policy"
        data["characteristics"] = "bisexual, transgender"
    elif role_type == "mentee":
        data["target profession"] = "Policy"
        data["match with similar identity"] = "yes"
        data["identity to match"] = "bisexual"
    else:
        raise ValueError
    return data


def random_data(role_type: str):
    data = {
        "first name": role_type,
        "last name": "",
        "email address": "",
        "both mentor and mentee": random.choice(["yes", "no"]),
        "job title": "Some role",
        "grade": grades()[random.randint(2, len(grades()) - 1)]
        if role_type == "mentor"
        else grades()[random.randint(0, len(grades()) - 2)],
        "organisation": (
            "Department of"
            f" {random.choice(['Fun', 'Truth', 'Joy', 'Love', 'Virtue', 'Peace'])}"
        ),
        "profession": random.choice(["Policy", "DDaT", "Operations", "HR", "Security"]),
    }
    if role_type == "mentor":
        characteristics = random.choice(
            [
                "",
                ", ".join(
                    random.sample(
                        [
                            "Asexual or aromantic",
                            "Gay",
                            "Lesbian",
                            "Bisexual or pansexual",
                            "Transgender",
                            "Non-binary",
                        ],
                        random.randint(1, 2),
                    )
                ),
            ]
        )
        data["characteristics"] = characteristics
    elif role_type == "mentee":
        data["match with similar identity"] = random.choice(["yes", "no"])
        data["identity to match"] = random.choice(
            [
                "",
                "Asexual or aromantic",
                "Gay",
                "Lesbian",
                "Bisexual or pansexual",
                "Transgender",
                "Non-binary",
            ]
        )
    else:
        raise ValueError
    return data


def rows_of_random_data(role_type: str, quantity: int = 50):
    rows = []
    padding_size = int(math.log10(quantity)) + 1
    for i in range(quantity):
        data = random_data(role_type)
        data["last name"] = str(i).zfill(padding_size)
        data["email address"] = f"{role_type}.{str(i).zfill(padding_size)}@gov.uk"
        data["biography"] = (
            f'My name is {data["first name"]} {data["last name"]}. I am a'
            f' {data["grade"]}. I am in the {data["organisation"]}, in the'
            f' {data["profession"]} profession. My characteristics is/are'
            f' {data.get("characteristics", data.get("identity to match"))}. '
        )
        rows.append(data.copy())
    return rows


def random_file(role_type: str, quantity: int = 50):
    data_path = f"{role_type}s.csv"
    with open(data_path, "w", newline="") as test_data:
        rows = rows_of_random_data(role_type, quantity)
        file_writer: csv.DictWriter[str] = csv.DictWriter(
            test_data, list(rows[0].keys())
        )
        file_writer.writeheader()
        file_writer.writerows(rows)


def base_rules() -> list[rl.Rule]:
    return [
        rl.Disqualify(
            lambda match: match.mentee.organisation == match.mentor.organisation
        ),
        rl.Disqualify(rl.Grade(target_diff=2, logical_operator=operator.gt).evaluate),
        rl.Disqualify(rl.Grade(target_diff=0, logical_operator=operator.le).evaluate),
        rl.Disqualify(lambda match: match.mentee in match.mentor.mentees),
        rl.Grade(2, operator.eq, {True: 12, False: 0}),
        rl.Grade(1, operator.eq, {True: 9, False: 0}),
        rl.Generic(
            {True: 10, False: 0},
            lambda match: match.mentee.target_profession
            == match.mentor.current_profession,
        ),
        rl.Generic(
            {True: 6, False: 0},
            lambda match: match.mentee.characteristic in match.mentor.characteristics
            and match.mentee.characteristic != "",
        ),
    ]
