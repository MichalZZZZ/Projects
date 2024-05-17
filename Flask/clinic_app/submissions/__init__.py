from flask import Blueprint

submission_bp = Blueprint('submissions', __name__)

from clinic_app.submissions import submissions