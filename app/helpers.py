import csv
import math
import pathlib
import string
import random


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
        else grades()[random.randint(0, len(grades()) - 3)],
        "organisation": (
            "Department of"
            f" {random.choice(['Fun', 'Truth', 'Joy', 'Love', 'Virtue', 'Peace'])}"
        ),
        "biography": "Test biography",
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
                        random.randint(1, 3),
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


def random_file(role_type: str, quantity: int = 50):
    data_path = f"{role_type}s.csv"
    with open(data_path, "w", newline="") as test_data:
        rows = []
        padding_size = int(math.log10(quantity)) + 1
        for i in range(quantity):
            data = random_data(role_type)
            data["last name"] = str(i).zfill(padding_size)
            data["email address"] = f"{role_type}.{str(i).zfill(padding_size)}@gov.uk"
            rows.append(data.copy())
        file_writer: csv.DictWriter[str] = csv.DictWriter(test_data, list(data.keys()))
        file_writer.writeheader()
        file_writer.writerows(rows)
