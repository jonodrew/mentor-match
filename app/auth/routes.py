import os

from app.auth import auth_bp
from flask import redirect, url_for, request, render_template, make_response


def valid_login(login_request):
    return login_request.form["username"] == os.getenv(
        "USERNAME"
    ) and login_request.form["password"] == os.getenv("PASSWORD")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        cookie = {"key": "logged-in", "value": "false"}
        if valid_login(request):
            cookie["value"] = "true"
            url = url_for("main.index")
        else:
            url = url_for("auth.login")
        response = make_response(redirect(url))
        response.set_cookie(**cookie)
        return response
