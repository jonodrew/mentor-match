import datetime
import os.path
from datetime import timedelta

from flask import (
    make_response,
    render_template,
    request,
    jsonify,
    current_app,
    url_for,
    send_from_directory,
    after_this_request,
)
import pathlib
import shutil

from werkzeug.utils import secure_filename, redirect

from app.extensions import celery
from app.main import main_bp
from app.helpers import valid_files, random_string
from app.tasks.tasks import async_process_data, delete_mailing_lists_after_period
from matching.factory import ParticipantFactory
from matching.mentee import Mentee
from matching.mentor import Mentor
from matching.process import create_participant_list_from_path, create_mailing_list


@main_bp.route("/", methods=["GET"])
def index():
    return render_template("index.html", title="Mentor matcher")


@main_bp.route("/cookies")
def cookies():
    return render_template("cookies.html", title="Cookies")


@main_bp.route("/privacy-and-data")
def privacy():
    return render_template("privacy-and-data.html", title="Privacy and data")


@main_bp.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        return render_template("input.html")
    if request.method == "POST":
        files = request.files.getlist("files")
        filenames = [file.filename for file in files]
        if len(files) == 2 and valid_files(filenames):
            folder = random_string()
            for file in files:
                pathlib.Path(current_app.config["UPLOAD_FOLDER"], folder).mkdir(
                    parents=True, exist_ok=True
                )
                filename = secure_filename(file.filename)
                file.save(
                    os.path.join(current_app.config["UPLOAD_FOLDER"], folder, filename)
                )
            response = make_response(redirect(url_for("main.process")))
            response.set_cookie(
                "data-folder",
                folder,
                expires=datetime.datetime.now() + timedelta(minutes=30),
            )
            return response
        else:
            if len(files) != 2:
                error_message = (
                    "Number of files is incorrect. Please only upload two files."
                )
            elif not valid_files(filenames):
                error_message = (
                    "Your filenames are incorrect. Please label your files as"
                    " 'mentees.csv' and 'mentors.csv'."
                )
            else:
                error_message = "Unspecified error. Please contact the admin team"
            return make_response(
                render_template("input.html", error_message=error_message), 415
            )


@main_bp.route("/download/<task_id>", methods=["GET"])
def download(task_id):
    @after_this_request
    def delete_files(response):
        period = int(os.getenv("DATA_STORAGE_PERIOD_SECS", 900))
        delete_mailing_lists_after_period.apply_async(
            (task_id,), eta=datetime.datetime.now() + timedelta(seconds=period)
        )
        return response

    return render_template("output.html", title="Download matches", data_folder=task_id)


@main_bp.route("/tasks", methods=["POST"])
def run_task():
    current_app.logger.debug(request.get_json())
    data_folder = request.get_json()["data_folder"]
    folder = pathlib.Path(
        os.path.join(current_app.config["UPLOAD_FOLDER"], data_folder)
    )

    @after_this_request
    def delete_upload(response):
        shutil.rmtree(folder)
        return response

    mentors = [
        mentor.to_dict()
        for mentor in create_participant_list_from_path(Mentor, path_to_data=folder)
    ]
    mentees = [
        mentee.to_dict()
        for mentee in create_participant_list_from_path(Mentee, path_to_data=folder)
    ]
    task = async_process_data.delay((mentors, mentees))
    return jsonify(task_id=task.id), 202


@main_bp.route("/tasks/status/<task_id>", methods=["GET"])
def get_status(task_id):
    """
    This route checks the status of the long-running celery task. Once the task is complete it returns the
    matched participants as JSON formatted data. This data is then fed into the `create_mailing_list` function,
     where the mailing lists are saved to a folder that corresponds to the `task_id`.
    """
    task_result = celery.AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": "processing",
    }
    if task_result.status == "SUCCESS":
        for matched_participant_list in task_result.result:
            participants = [
                ParticipantFactory.create_from_dict(participant_dict)
                for participant_dict in matched_participant_list
            ]
            create_mailing_list(
                participants,
                pathlib.Path(
                    os.path.join(current_app.config["UPLOAD_FOLDER"], task_id)
                ),
            )
            result["task_result"] = url_for("main.download", task_id=task_id)
    return result, 200


@main_bp.route("/tasks/<task_id>", methods=["GET", "DELETE"])
def tasks(task_id):
    """
    This does two things:
    on GET: the data in the path `pathlib.Path(current_app.config["UPLOAD_FOLDER"], task_id)` is zipped and served to
    the  user. Following this request, the data and the zipped data are deleted.
    on DELETE: the server attempts to delete the data in the path
    `pathlib.Path(current_app.config["UPLOAD_FOLDER"], task_id) and returns either a 202 if successful or a 404 if the
    file doesn't exist
    :param task_id:
    :return:
    """
    if request.method == "GET":

        @after_this_request
        def remove_files(response):
            shutil.rmtree(pathlib.Path(current_app.config["UPLOAD_FOLDER"], task_id))
            os.remove(
                pathlib.Path(current_app.config["UPLOAD_FOLDER"], f"{task_id}.zip")
            )
            return response

        data_path = pathlib.Path(current_app.config["UPLOAD_FOLDER"], task_id)
        current_app.logger.debug(data_path)
        shutil.make_archive(
            base_name=data_path,
            format="zip",
            root_dir=data_path,
        )
        return send_from_directory(
            directory=pathlib.Path(current_app.config["UPLOAD_FOLDER"]),
            path=f"{task_id}.zip",
        )
    elif request.method == "DELETE":
        try:
            shutil.rmtree(pathlib.Path(current_app.config["UPLOAD_FOLDER"], task_id))
            status_code = 202
        except FileNotFoundError:
            status_code = 404
        return jsonify(), status_code


@main_bp.route("/process", methods=["GET"])
def process():
    if not request.cookies.get("data-folder"):
        return redirect(url_for("main.upload"))
    else:
        return render_template("process.html")


@main_bp.route("/finished", methods=["GET"])
def finished():
    return render_template("done.html")
