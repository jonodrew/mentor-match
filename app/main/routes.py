from flask import render_template, request, jsonify
from tasks.tasks import create_task
from extensions import celery

from app.main import main_bp



@main_bp.route("/", methods=["GET"])
def index():
    return render_template("index.html", title="Hello World!")


@main_bp.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        return render_template("input.html")
    if request.method == "POST":
        task = create_task.delay(int("1"))
        return jsonify(task_id="1"), 202


@main_bp.route("/tasks", methods=["POST"])
def run_task():
    content = request.json
    task_type = content["type"]
    task = create_task.delay(int(task_type))
    return {"task_id": task.id}, 202


@main_bp.route("/tasks/<task_id>", methods=["GET"])
def get_status(task_id):
    task_result = celery.AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result,
    }
    return result, 200
