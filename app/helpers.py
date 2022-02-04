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
