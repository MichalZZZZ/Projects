from flask import Blueprint

admin_bp = Blueprint('admin', __name__)

from clinic_app.admin import admin