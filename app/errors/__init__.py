from flask import Blueprint

error_bp = Blueprint("error", __name__)

from app.main import routes  # noqa: E402,F401
