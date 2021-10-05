from celery.result import AsyncResult
from flask import render_template, request

from app.main import main_bp



@main_bp.route("/", methods=["GET"])
def index():
    return render_template("index.html", title="Hello World!")


@main_bp.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        return render_template("input.html")


@main_bp.route("/tasks", methods=["POST"])
def run_task():
    content = request.json
    task_type = content["type"]
    task = create_task.delay(int(task_type))
    return {"task_id": task.id}, 202


@main_bp.route("/tasks/<task_id>", methods=["GET"])
def get_status(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result,
    }
    return result, 200
