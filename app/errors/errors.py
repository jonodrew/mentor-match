from flask import render_template
from app.errors import error_bp


@error_bp.errorhandler(404)
def resource_not_found(error):
    return render_template("page_not_found.html"), 404
