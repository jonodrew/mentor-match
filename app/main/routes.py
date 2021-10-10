import pathlib
import shutil

from flask import render_template, request, jsonify, current_app, url_for, send_from_directory, \
    after_this_request

from app.extensions import celery
from app.main import main_bp
from app.tasks.tasks import create_task, process_data
from matching.factory import ParticipantFactory
from matching.mentee import Mentee
from matching.mentor import Mentor
from matching.process import create_participant_list_from_path, create_mailing_list


@main_bp.route("/", methods=["GET"])
def index():
    return render_template("index.html", title="Hello World!")


@main_bp.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        return render_template()
    if request.method == "POST":
        task = create_task.delay(int("1"))
        return jsonify(task_id="1"), 202


@main_bp.route("/download/<task_id>", methods=["GET", "POST"])
def download(task_id):
    data_path = f"/app/static/{task_id}/"
    if request.method == "GET":
        shutil.make_archive("".join((data_path, task_id)), 'zip', data_path)
        return render_template("output.html")
    if request.method == "POST":
        @after_this_request
        def remove_file(response):
            try:
                shutil.rmtree(data_path)
            except Exception as error:
                current_app.logger.error("Error removing or closing downloaded file handle", error)
            return response

        return send_from_directory(data_path, f"{task_id}.zip")


@main_bp.route("/tasks", methods=["POST"])
def run_task():
    mentors = [mentor.to_dict() for mentor in
               create_participant_list_from_path(Mentor, pathlib.Path("/app/static/data"))]
    mentees = [mentee.to_dict() for mentee in
               create_participant_list_from_path(Mentee, pathlib.Path("/app/static/data"))]
    task = process_data.delay((mentors, mentees))
    return jsonify(task_id=task.id), 202


@main_bp.route("/tasks/<task_id>", methods=["GET"])
def get_status(task_id):
    task_result = celery.AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": "Processing",
    }
    if task_result.status == "SUCCESS":
        for matched_participant_list in task_result.result:
            participants = [ParticipantFactory.create_from_dict(participant_dict) for participant_dict in
                            matched_participant_list]
            create_mailing_list(participants, pathlib.Path(f"app/static/{task_id}"))
            result["task_result"] = f'<a href={url_for("main.download", task_id=task_id)}><button>Download ' \
                                    'results</button></a> '
    return result, 200
