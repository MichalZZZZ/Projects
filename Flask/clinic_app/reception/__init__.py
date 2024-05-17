from flask import Blueprint

reception_bp = Blueprint('reception', __name__)

from clinic_app.reception import reception