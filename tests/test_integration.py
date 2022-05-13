import csv
import os.path
import pathlib
import time
from unittest.mock import patch

import pytest
from flask import current_app, url_for, request
from matching.process import create_participant_list_from_path

from app.classes import CSMentee, CSMentor
from app.tasks.tasks import async_process_data


@pytest.mark.integration
class TestIntegration:
    def test_input_data(
        self,
        test_participants,
        test_data_path,
        celery_worker,
        celery_app,
        client,
    ):
        src_file_paths = (
            test_data_path / "mentees.csv",
            test_data_path / "mentors.csv",
        )
        files = []
        patched_random = patch("app.main.routes.random_string", return_value="abcdef")
        patched_random.start()
        try:
            files = [open(fpath, "rb") for fpath in src_file_paths]
            resp = client.post(
                "/upload",
                data={
                    "files": files,
                },
                follow_redirects=True,
            )
        finally:
            for fp in files:
                fp.close()
        patched_random.stop()
        cookie_value = request.cookies.get("data-folder")
        assert resp.status_code == 200
        assert cookie_value == "abcdef"

    def test_process_data(self, celery_app, celery_worker, known_file, test_data_path):
        known_file(test_data_path, "mentee", 50)
        known_file(test_data_path, "mentor", 50)
        mentees = [
            mentee.to_dict()
            for mentee in create_participant_list_from_path(CSMentee, test_data_path)
        ]
        mentors = [
            mentor.to_dict()
            for mentor in create_participant_list_from_path(CSMentor, test_data_path)
        ]
        task = async_process_data.delay((mentors, mentees), [])
        while not task.state == "SUCCESS":
            time.sleep(1)
        assert len(task.result[0]) == 50

    @pytest.mark.parametrize(["test_task", "output"], [("small", 10), ("large", 100)])
    def test_create_mailing_list(
        self,
        celery_app,
        celery_worker,
        known_file,
        test_data_path,
        test_task,
        output,
        client,
    ):
        known_file(pathlib.Path(test_data_path, test_task), "mentee", output)
        known_file(pathlib.Path(test_data_path, test_task), "mentor", output)
        processing_id = client.post(
            "/tasks", json={"data_folder": test_task}
        ).get_json()["task_id"]

        resp = client.get(url_for("main.get_status", task_id=processing_id))
        content = resp.get_json()
        assert content == {
            "task_id": processing_id,
            "task_status": "PENDING",
            "task_result": "processing",
        }
        assert resp.status_code == 200
        current_app.config["UPLOAD_FOLDER"] = test_data_path
        while content["task_status"] == "PENDING":
            time.sleep(1)
            resp = client.get(url_for("main.get_status", task_id=processing_id))
            content = resp.get_json()
        assert pathlib.Path(
            os.path.join(current_app.config["UPLOAD_FOLDER"]), processing_id
        ).exists()
        with open(
            pathlib.Path(
                os.path.join(current_app.config["UPLOAD_FOLDER"]),
                processing_id,
                "mentors-list.csv",
            )
        ) as csv_file:
            reader = csv.DictReader(csv_file)
            assert list(next(reader).keys()) == [
                "first name",
                "last name",
                "email address",
                "number of matches",
                "mentor only",
                "mentee only",
                "both mentor and mentee",
                "match 0 biography",
                "match 1 biography",
                "match 2 biography",
                "match details",
            ]

    def test_delete_route(self, client, known_file, test_data_path):
        for participant in ("mentor", "mentee"):
            known_file(
                pathlib.Path(current_app.config["UPLOAD_FOLDER"], "12345"),
                participant,
                50,
            )
        assert os.path.exists(
            pathlib.Path(current_app.config["UPLOAD_FOLDER"], "12345", "mentors.csv")
        )
        client.delete(url_for("main.tasks", task_id="12345"))
        assert not os.path.exists(
            pathlib.Path(current_app.config["UPLOAD_FOLDER"], "12345", "mentors.csv")
        )
