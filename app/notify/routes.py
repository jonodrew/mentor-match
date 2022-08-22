import csv
import os
import pathlib

import celery
import werkzeug as werkzeug
from flask import (
    render_template,
    request,
    redirect,
    make_response,
    Response,
    current_app,
    url_for,
    abort,
)

from app.export import ExportFactory
from app.helpers import get_data_folder_path
from app.notify import notify_bp
from app.tasks.tasks import send_notification


@notify_bp.route("/notify-settings/before-you-start", methods=["GET"])
def notify_settings_before_you_start():
    return render_template("notify-settings/notify-settings-intro.html")


@notify_bp.route("/notify-settings/template-ids", methods=["GET"])
def notify_settings_template_id():
    return render_template("notify-settings/notify-settings--template-ids.html")


@notify_bp.route("/notify-settings/reply-to", methods=["GET", "POST"])
def notify_settings_reply_id():
    response = make_response(
        render_template("notify-settings/notify-settings--reply-to.html")
    )
    if request.method == "POST":
        for name, value in request.form.items():
            response.set_cookie(
                name,
                value,
            )
    return response


@notify_bp.route("/notify-settings/api-key", methods=["GET", "POST"])
def notify_settings_api_key():
    response = make_response(
        render_template("notify-settings/notify-settings--api-key.html")
    )
    if request.method == "POST":
        for name, value in request.form.items():
            response.set_cookie(name, value)
    return response


@notify_bp.route("/notify-settings/done", methods=["POST"])
def notify_settings_done():
    queue_emails()
    return redirect(url_for("main.index"))


def queue_emails():
    service = request.cookies.get("service", "notify")
    data_folder = request.cookies["task-id"]
    if (data_path := get_data_folder_path(current_app, data_folder)).exists():
        try:
            exporter = ExportFactory.create_exporter(
                service, api_key=request.form.get("api-key-field"), **request.cookies
            )
        except AssertionError as e:
            current_app.logger.info(e)
            raise werkzeug.exceptions.BadRequest(
                "The API key you have provided is not recognised"
            )
        for string in ("csmentors-list.csv", "csmentees-list.csv"):
            with open(pathlib.Path(os.path.join(data_path, string))) as participant_csv:
                reader = csv.DictReader(participant_csv)
                batch = celery.group(
                    send_notification.si(exporter, participant)
                    for participant in reader
                ).apply_async()
        return Response(response=batch.id, status=201)
    else:
        abort(404, "That data doesn't exist")
