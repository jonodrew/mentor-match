from flask import Blueprint

notify_bp = Blueprint("notify", __name__, url_prefix="/notify")

from app.notify import routes  # noqa: E402,F401
