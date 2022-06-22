from unittest.mock import patch
import pytest
from flask import url_for


class TestNotifyRoute:
    @pytest.mark.unit
    @patch("app.main.routes.ExportFactory", autospec=True)
    def test_when_route_passed_form_creates_exporter(self, patched_factory, client):
        patch("app.main.routes.celery.group").start()
        client.set_cookie(server_name="localhost", key="data-folder", value="test")
        with patch.object(patched_factory, "create_exporter") as patched_creator:
            client.post(url_for("main.notify_participants"), data={"service": "notify"})
            patched_creator.assert_called_with("notify")

    def test_notify_route_reads_all_user_data(self):
        assert False
