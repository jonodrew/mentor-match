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
                patched_creator.assert_called_with(
                    "notify",
                )
