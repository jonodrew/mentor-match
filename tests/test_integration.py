import os.path
import pathlib
import time

import pytest
from flask import current_app
from matching.mentee import Mentee
from matching.mentor import Mentor
from matching.process import create_participant_list_from_path

from app.tasks.tasks import async_process_data


@pytest.mark.skipif(
    os.environ.get("ENV") != "integration",
    reason="These tests require a running instance of a backing service",
)
class TestIntegration:
    @pytest.mark.skip(reason="Input isn't written yet")
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
        try:
            files = [open(fpath, "rb") for fpath in src_file_paths]
            resp = client.post(
                "/upload",
                data={
                    "files": files,
                },
            )
        finally:
            for fp in files:
                fp.close()

        content = resp.get_json()
        task_id = content["task_id"]
        assert resp.status_code == 202
        assert task_id == "1"

        processing_id = client.post("/tasks", data={"task_id": "small"}).get_json()[
            "task_id"
        ]
        current_app.config["UPLOAD_FOLDER"] = test_data_path
        resp = client.get(f"/tasks/{processing_id}")
        content = resp.get_json()
        assert content == {"task_id": processing_id, "task_status": "PENDING"}
        assert resp.status_code == 200

        while content["task_status"] == "PENDING":
            time.sleep(1)
            resp = client.get(f"/tasks/{processing_id}")
            content = resp.get_json()
        assert content == {
            "task_id": processing_id,
            "task_status": "SUCCESS",
            "task_result": True,
        }

    def test_process_data(self, celery_app, celery_worker, known_file, test_data_path):
        known_file(test_data_path, "mentee", 50)
        known_file(test_data_path, "mentor", 50)
        mentees = [
            mentee.to_dict()
            for mentee in create_participant_list_from_path(Mentee, test_data_path)
        ]
        mentors = [
            mentor.to_dict()
            for mentor in create_participant_list_from_path(Mentor, test_data_path)
        ]
        task = async_process_data.delay((mentors, mentees))
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
        processing_id = client.post("/tasks", json={"task_id": test_task}).get_json()[
            "task_id"
        ]
        current_app.config["UPLOAD_FOLDER"] = test_data_path
        resp = client.get(f"/tasks/{processing_id}")
        content = resp.get_json()
        assert content == {
            "task_id": processing_id,
            "task_status": "PENDING",
            "task_result": "processing",
        }
        assert resp.status_code == 200

        while content["task_status"] == "PENDING":
            time.sleep(1)
            resp = client.get(f"/tasks/{processing_id}")
            content = resp.get_json()
        assert pathlib.Path(
            os.path.join(current_app.config["UPLOAD_FOLDER"]), processing_id
        ).exists()
