from flask import Blueprint

errors_bp = Blueprint('errors', __name__)

from clinic_app.errors import errors