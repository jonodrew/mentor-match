from flask import render_template, request

from app.main import main_bp


@main_bp.route("/", methods=["GET"])
def index():
    return render_template("index.html", title="Hello World!")


@main_bp.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        return render_template()
