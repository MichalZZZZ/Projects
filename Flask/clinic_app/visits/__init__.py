from flask import Blueprint

visit_bp = Blueprint('visits', __name__)

from clinic_app.visits import visits