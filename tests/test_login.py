from unittest.mock import patch

import pytest
from flask import url_for


@pytest.mark.unit
def test_login(client):
    with patch(
        "app.main.routes.os.getenv", side_effect=["CSLGBT", "BatteryHorseStapleCorrect"]
    ):
        client.delete_cookie("localhost", "logged-in", "true")
        response = client.post(
            url_for("auth.login"),
            data={"username": "CSLGBT", "password": "BatteryHorseStapleCorrect"},
            follow_redirects=True,
        )
    assert response.request.path == url_for("main.index")
