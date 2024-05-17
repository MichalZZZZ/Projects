from flask import Blueprint

patient_bp = Blueprint('patients', __name__)

from clinic_app.patients import patients