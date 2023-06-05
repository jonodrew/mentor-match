from flask import Blueprint

main_bp = Blueprint("main", __name__)


# @main_bp.before_request
# def check_login():
#     if not (request.cookies.get("logged-in") or request.path == url_for("auth.login")):
#         return redirect(url_for("auth.login"))


from app.main import routes  # noqa: E402,F401
