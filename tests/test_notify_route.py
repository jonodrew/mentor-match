from unittest.mock import patch

import mock
import pytest
from flask import url_for


@pytest.fixture
def notify_client(client):
    client.set_cookie(server_name="localhost", key="task-id", value="data")
    yield client


@pytest.fixture
def patch_open_file():
    data = mock.mock_open(read_data="first,second,third")
    with patch(target="app.main.routes.open", new=data):
        yield


@pytest.fixture
def patch_csv_reader():
    with patch("app.main.routes.csv.DictReader", return_value=({} for _ in range(10))):
        yield


class TestNotifyRoute:
    @pytest.mark.unit
    @patch("app.main.routes.ExportFactory", autospec=True)
    def test_when_route_passed_form_creates_exporter(
        self, patched_factory, client, patch_open_file
    ):
        with patch("app.main.routes.celery.group"):
            with patch.object(patched_factory, "create_exporter") as patched_creator:
                client.post(
                    url_for("main.notify_participants"), data={"service": "notify"}
                )
                patched_creator.assert_called_with("notify")

    @pytest.mark.unit
    def test_notify_route_reads_all_user_data(
        self, patch_open_file, test_data_path, client, patch_csv_reader
    ):
        with patch(
            "app.main.routes.celery.group", autospec=True
        ) as patched_celery_group:
            with patch("app.main.routes.send_notification.si") as patched_notification:
                client.post(
                    url_for("main.notify_participants"),
                    data={
                        "service": "notify",
                        "api-key": "".join(str(_) for _ in range(100)),
                    },
                )
                assert patched_celery_group.call_count == 2
                mentors_call, mentees_call = patched_celery_group.call_args_list
                args, kwargs = mentors_call
                calls = list(args[0])
                assert len(calls) == 10
                notification_args = patched_notification.call_args
                assert notification_args[1] == {}

    @pytest.mark.unit
    def test_notify_route_raises_404_if_no_data(self, notify_client):
        response = notify_client.post(
            url_for("main.notify_participants"),
            data={
                "service": "notify",
                "api-key": "".join(str(_) for _ in range(100)),
            },
        )
        assert response.status_code == 404
