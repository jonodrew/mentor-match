from typing import Sequence


def valid_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() == "csv"


def mentors_and_mentees_present(filenames: list[str]) -> bool:
    return set(map(lambda filename: filename.rsplit(".", 1)[0].lower(), filenames)) == {
        "mentors",
        "mentees",
    }


def valid_files(filenames: Sequence[str]) -> bool:
    return mentors_and_mentees_present(filenames) and all(map(valid_file, filenames))
