import os
import pathlib
from flask import current_app, url_for


def test_mailing_lists_deleted_after_get_request(client, test_data_path):
    """This test writes two files to the test web app's upload folder. It then checks that these files are deleted
    once the download route is called."""

    def write_test_file(filename):
        filepath = pathlib.Path(test_data_path, "12345", filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        f = open(filepath, "w")
        f.write("Fake data")
        f.close()

    for filename in ("mentors.csv", "mentees.csv"):
        write_test_file(filename)
    assert os.path.exists(pathlib.Path(test_data_path, "12345", "mentors.csv"))
    response = client.get(url_for("main.download_task", task_id="12345"))
    assert response.status_code == 200
    assert not os.path.exists(
        pathlib.Path(current_app.config["UPLOAD_FOLDER"], "12345", "mentors.csv")
    )
    assert not os.path.exists(
        pathlib.Path(current_app.config["UPLOAD_FOLDER"], "12345.zip")
    )
