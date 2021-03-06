import pytest
from flask import url_for


@pytest.mark.unit
def test_no_data_folder_in_session_redirects_to_input(client):
    response = client.get(url_for("main.process"), follow_redirects=True)
    assert response.request.path != url_for("main.process")
    assert response.request.path == url_for("main.upload")
