from clinic_app import create_app
from flask_cors import CORS

application = create_app('production')
CORS(application)