import json
from unittest.mock import patch

import pytest

from app import create_app
from app.config import TestConfig


@pytest.mark.skip
def test_input_output_data(test_participants, test_data_path, celery_worker, celery_app):
    with patch("app.extensions.celery", celery_app):
        app = create_app(TestConfig)
        with app.test_client() as client:
            src_file_paths = (test_data_path / "mentees.csv", test_data_path / "mentors.csv")
            files = []
            try:
                files = [open(fpath, 'rb') for fpath in src_file_paths]
                resp = client.post('/upload', data={
                    'files': files,
                })
            finally:
                for fp in files:
                    fp.close()

            content = json.loads(resp.data.decode())
            task_id = content["task_id"]
            assert resp.status_code == 202
            assert task_id

            resp = client.get(f"tasks/{task_id}")
            content = json.loads(resp.data.decode())
            assert content == {"task_id": task_id, "task_status": "PENDING", "task_result": None}
            assert resp.status_code == 200

            while content["task_status"] == "PENDING":
                resp = client.get(f"tasks/{task_id}")
                content = json.loads(resp.data.decode())
            assert content == {"task_id": task_id, "task_status": "SUCCESS", "task_result": True}