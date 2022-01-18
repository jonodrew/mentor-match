import os

import flask

from app.auth import auth_bp
from flask import redirect, url_for
import google_auth_oauthlib.flow  # type: ignore


CONFIG = {
    "web": {
        "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
        "project_id": "mentor-match-333011",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
    }
}


@auth_bp.route("/login", methods=["GET", "POST"])
def authorize():
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        client_config=CONFIG,
        scopes=["https://www.googleapis.com/auth/drive"],
    )
    flow.redirect_uri = url_for("auth.callback", _external=True)
    authorization_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true"
    )
    flask.session["state"] = state
    return redirect(authorization_url)


@auth_bp.route("/callback", methods=["GET"])
def callback():
    state = flask.session["state"]
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        client_config=CONFIG,
        scopes=["https://www.googleapis.com/auth/drive"],
        state=state,
    )
    flow.redirect_uri = flask.url_for("auth.callback", _external=True)

    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    flask.session["credentials"] = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }
    return redirect(url_for("main.upload"))
