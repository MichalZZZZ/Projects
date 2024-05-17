from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail


db = SQLAlchemy()
migrate = Migrate()
mail = Mail()


def create_app(config_name='development') -> object:
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    if config_name == 'testing':
        from clinic_app.admin import admin_bp
        app.register_blueprint(admin_bp, url_prefix='/api/admin')

    from clinic_app.commands import db_manage_bp
    from clinic_app.errors import errors_bp
    from clinic_app.auth import auth_bp
    from clinic_app.patients import patient_bp
    from clinic_app.doctors import doctor_bp
    from clinic_app.reception import reception_bp
    from clinic_app.submissions import submission_bp
    from clinic_app.visits import visit_bp

    app.register_blueprint(db_manage_bp)
    app.register_blueprint(errors_bp)
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(patient_bp, url_prefix='/api/patients')
    app.register_blueprint(doctor_bp, url_prefix='/api/doctors')
    app.register_blueprint(reception_bp, url_prefix='/api/reception')
    app.register_blueprint(submission_bp, url_prefix='/api/submissions')
    app.register_blueprint(visit_bp, url_prefix='/api/visits')

    return app
