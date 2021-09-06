import argparse
import logging
import sys
from pathlib import Path

from matching.process import conduct_matching, create_mailing_list

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
root.addHandler(handler)


def main():
    parser = argparse.ArgumentParser(
        description='Match mentors to mentees. Your files should be called "mentees.csv" and "mentors.csv".'
    )
    parser.add_argument(
        "filepath", type=str, help="the path to the data containing the files"
    )
    path_to_data = Path(parser.parse_args().filepath)
    logging.info("Beginning matching exercise. This might take up to five minutes.")
    mentors, mentees = conduct_matching(path_to_data)
    logging.log("Matches found. Exporting to output folder!")
    out_put_folder = path_to_data / "output"
    create_mailing_list(mentors, out_put_folder)
    create_mailing_list(mentees, out_put_folder)


if __name__ == "__main__":
    main()
