from unittest.mock import patch

import werkzeug.exceptions
from flask import url_for


def test_error_raised_on_file_not_found_error(client):
    with patch("app.main.routes.json.loads", side_effect=werkzeug.exceptions.NotFound):
        response = client.get(url_for("main.download", task_id="12345"))
        assert response.status_code == 404
