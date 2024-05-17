from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from clinic_app.auth import auth