from flask import Blueprint

doctor_bp = Blueprint('doctors', __name__)

from clinic_app.doctors import doctors
