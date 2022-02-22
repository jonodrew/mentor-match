import pathlib
from unittest.mock import patch, Mock, MagicMock

import pytest
from flask import url_for, session
from app.tasks.tasks import delete_mailing_lists_after_period


@pytest.mark.unit
def test_when_processing_uploaded_data_deleted(client, test_data_path, write_test_file):
    for filename in ("mentors.csv", "mentees.csv"):
        write_test_file(filename)
    assert pathlib.Path(test_data_path, "12345").exists()
    session["data-folder"] = "12345"
    mock_task = Mock()
    mock_task.id = 1
    with patch("app.main.routes.async_process_data.delay", return_value=mock_task):
        client.post(url_for("main.run_task"), json={"data_folder": "12345"})
        assert not pathlib.Path(test_data_path, "12345").exists()


@pytest.mark.unit
@patch("app.tasks.tasks.requests.delete", return_value=MagicMock, autospec=True)
def test_delete_calls_correct_path(patched_delete):
    delete_mailing_lists_after_period("12345")
    patched_delete.assert_called_with("localhost:5001/12345")
