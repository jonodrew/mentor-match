import flask

from app.auth import auth_bp
from flask import redirect, url_for
import google_auth_oauthlib.flow


@auth_bp.route("/login", methods=["GET", "POST"])
def authorize():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        "client_secret_655796018812-7t5put9apqg7sas5j6c0e9bgcc224lem.apps.googleusercontent.com.json",
        scopes=["https://www.googleapis.com/auth/drive"],
    )
    flow.redirect_uri = "http://localhost:5001/callback"
    authorization_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true"
    )
    flask.session["state"] = state
    return redirect(authorization_url)


@auth_bp.route("/callback", methods=["GET"])
def callback():
    state = flask.session["state"]
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        "client_secret_655796018812-7t5put9apqg7sas5j6c0e9bgcc224lem.apps.googleusercontent.com.json",
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
