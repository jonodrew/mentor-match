import pathlib
from unittest.mock import patch, Mock, MagicMock

import pytest
from flask import url_for, session
from app.tasks.tasks import delete_mailing_lists_after_period, async_process_data


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
def test_delete_calls_correct_path():
    with patch(
        "app.tasks.tasks.requests.delete", return_value=MagicMock()
    ) as patched_delete:
        patched_delete.status_code.return_value = 202
        delete_mailing_lists_after_period("12345")
        patched_delete.assert_called_with("http://app:5000/tasks/12345")


@pytest.mark.unit
def test_async_process_data(base_mentee_data, base_mentor_data):
    test_data = ([{"csmentor": base_mentor_data}], [{"csmentee": base_mentee_data}])
    assert async_process_data(data_to_process=test_data)
