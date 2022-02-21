import datetime
import os
import pathlib
from unittest.mock import patch

import pytest
from flask import current_app, url_for
import freezegun


@pytest.mark.unit
def test_mailing_lists_deleted_after_get_request(
    client, test_data_path, write_test_file
):
    """This test writes two files to the test web app's upload folder. It then checks that these files are deleted
    once the download route is called."""

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


@pytest.mark.unit
@patch("app.main.routes.delete_mailing_lists_after_period.apply_async")
def test_download_also_calls_async_delete_method(patched_async_delete, client):
    with freezegun.freeze_time(datetime.datetime(2022, 2, 22, 12, 1)):
        client.get(url_for("main.download", task_id="12345"))
        patched_async_delete.assert_called_with(
            ("12345",), eta=datetime.datetime(2022, 2, 22, 12, 16)
        )
