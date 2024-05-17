import jwt
from flask import current_app
from clinic_app import db
from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import datetime, date, timedelta
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True, index=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(255), nullable=False)

    @staticmethod
    def generate_hashed_password(password: str) -> str:
        return generate_password_hash(password)

    def generate_jwt(self):
        payload = {
            'user_id': self.id,
            'role': self.role,
            'exp': datetime.utcnow() + timedelta(minutes=current_app.config.get('JWT_EXPIRED_MINUTES', 330))
        }
        return jwt.encode(payload, current_app.config.get('SECRET_KEY'))

    def is_password_valid(self, password: str) -> bool:
        return check_password_hash(self.password, password)
    
    @staticmethod
    def additional_validation(param: str, value: str) -> str:
        return value

class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True, validate=validate.Length(min=3, max=255))
    email = fields.Email(required=True, validate=validate.Length(min=3, max=255))
    password = fields.String(required=True, validate=validate.Length(min=6, max=255))
    confirm_password = fields.String(required=True, validate=validate.Length(min=6, max=255))
    creation_date = fields.DateTime(dump_only=True)
    role = fields.String(dump_only=True, validate=validate.OneOf(['patient', 'doctor', 'receptionist', 'admin']))

    @validates('role')
    def validate_role(self, role):
        if role not in ['patient', 'doctor', 'receptionist', 'admin']:
            raise ValidationError('Invalid role')
        
class UserLoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)

class UserPasswordUpdateSchema(Schema):
    current_password = fields.String(required=True, load_only=True, validate=validate.Length(min=6, max=255))
    new_password = fields.String(required=True, load_only=True, validate=validate.Length(min=6, max=255))
    confirm_new_password = fields.String(required=True, load_only=True, validate=validate.Length(min=6, max=255))

class UserUsernameUpdateSchema(Schema):
    new_username = fields.String(required=True, validate=validate.Length(min=3, max=255))
    password = fields.String(required=True)

class UserPasswordAuthorizationSchema(Schema):
    password = fields.String(required=True)
    confirm_password = fields.String(required=True)



class Patient(db.Model):
    __tablename__ = 'Patients'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    pesel = db.Column(db.String(11), nullable=False, unique=True)
    phone_number = db.Column(db.String(9), nullable=False, unique=True)
    address = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=True)
    user = db.relationship('User', backref='patient')

    @staticmethod
    def additional_validation(param: str, value: str) -> str:
        return value

class PatientSchema(Schema):
    id = fields.Integer(dump_only=True)
    first_name = fields.String(required=True, validate=validate.Length(min=2, max=255))
    last_name = fields.String(required=True, validate=validate.Length(min=2, max=255))
    pesel = fields.String(required=True, validate=validate.Regexp(regex=r'^\d{11}$', error='Invalid PESEL format.'))
    phone_number = fields.String(required=True, validate=validate.Regexp(regex=r'^\d{9}$', error='Invalid phone number format.'))
    address = fields.String(required=True, validate=validate.Length(min=3, max=255))
    date_of_birth = fields.Date(format='%d-%m-%Y', dump_only=True)
    user_id = fields.Integer(dump_only=True)
    user = fields.Nested(UserSchema, only=['username', 'email'])

class PhoneNumberUpdate(Schema):
    phone_number = fields.String(required=True, validate=validate.Regexp(regex=r'^\d{9}$', error='Invalid phone number format.'))


class Token(db.Model):
    __tablename__ = 'Tokens'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255))
    user_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TokenSetPassword(db.Model):
    __tablename__ = 'Tokensetpassword'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255))
    email = db.Column(db.String(255))
    user_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Specialty(db.Model):
    __tablename__ = 'Specialties'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class SpecialtySchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(max=50))


class Hour(db.Model):
    __tablename__ = 'Hours'
    id = db.Column(db.Integer, primary_key=True)
    hour = db.Column(db.String)

class HourSchema(Schema):
    id = fields.Integer(dump_only=True)
    hour = fields.String(required=True)

class Doctor(db.Model):
    __tablename__ = 'Doctors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.relationship('User', backref='doctor')
    seniority = db.Column(db.String(15), nullable=False)
    description = db.Column(db.String, nullable=False)
    specialty_id = db.Column(db.Integer, db.ForeignKey('Specialties.id'), nullable=False)
    specialty = db.relationship('Specialty', backref='Doctors')
    photo = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id', ondelete='CASCADE'), nullable=False, unique=True)

    @staticmethod
    def additional_validation(param: str, value: str) -> str:
        return value

class DoctorSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=2, max=255))
    last_name = fields.String(required=True, validate=validate.Length(min=2, max=255))
    seniority = fields.String(required=True, validate=validate.Length(max=10))
    description = fields.String(required=True, validate=validate.Length(min=2, max=255))
    specialty_id = fields.Integer(load_only=True)
    specialty = fields.Nested('SpecialtySchema', only=['name'])
    photo = fields.String(required=True, validate=validate.Length(min=2, max=255))
    email = fields.Nested(UserSchema, only=['email'])
    user_id = fields.Integer(load_only=True)


class Reception(db.Model):
    __tablename__ = 'Receptions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(9), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id', ondelete='CASCADE'), nullable=True, unique=True)

class ReceptionSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=2, max=255))
    last_name = fields.String(required=True, validate=validate.Length(min=2, max=255))
    phone_number = fields.String(required=True, validate=validate.Regexp(regex=r'^\d{9}$', error='Invalid phone number format.'))
    user_id = fields.Integer(required=True)


class Submission(db.Model):
    __tablename__ = 'Submissions'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('Patients.id'), nullable=False)
    patient = db.relationship('Patient', backref='Submissions')
    doctor_id = db.Column(db.Integer, db.ForeignKey('Doctors.id', ondelete='CASCADE'), nullable=False)
    doctor = db.relationship('Doctor', backref='Submissions')
    status = db.Column(db.String(20), nullable=False, default='waiting')
    medications_used = db.Column(db.String(255), nullable=False)
    symptoms = db.Column(db.String(255), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    day = db.Column(db.Date, nullable=False)
    hour = db.Column(db.Time, nullable=False)

    @staticmethod
    def additional_validation(param: str, value: str) -> str:
        return value
    
class SubmissionSchema(Schema):
    id = fields.Integer(dump_only=True)
    number = fields.Integer()
    patient_id = fields.Integer(load_only=True)
    patient = fields.Nested('PatientSchema', only=['id', 'first_name', 'last_name', 'pesel', 'phone_number', 'address', 'user'])
    doctor_id = fields.Integer(load_only=True)
    doctor = fields.Nested('DoctorSchema', only=['name', 'last_name', 'specialty'])
    status = fields.String(dump_only=True)
    medications_used = fields.String(required=True, validate=validate.Length(min=2, max=255))
    symptoms = fields.String(required=True, validate=validate.Length(min=2, max=255))
    created_date = fields.DateTime(dump_only=True, format='%d-%m-%Y %H:%M')
    day = fields.Date(required=True, format='%d-%m-%Y')
    hour = fields.Time(required=True, format='%H:%M')

class CorrectnessSubmissionSchema(Schema):
    status = fields.String(required=True, validate=validate.OneOf(['accepted', 'rejected', 'canceled']))
    message = fields.String(required=False)


class Visit(db.Model):
    __tablename__ = 'Visits'
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('Submissions.id'), nullable=False)
    submission = db.relationship('Submission', backref='Visits')
    recommendations = db.Column(db.String(255), nullable=False)
    drugs = db.Column(db.String(255), nullable=False)
    diagnosis = db.Column(db.String(255), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def additional_validation(param: str, value: str) -> str:
        return value

class VisitSchema(Schema):
    id = fields.Integer(dump_only=True)
    submission_id = fields.Integer(load_only=True)
    submission = fields.Nested('SubmissionSchema', only=['number', 'patient', 'doctor', 'medications_used', 'symptoms', 'day', 'hour'])
    recommendations = fields.String(required=True, validate=validate.Length(min=2, max=255))
    drugs = fields.String(required=True, validate=validate.Length(min=2, max=255))
    diagnosis = fields.String(required=True, validate=validate.Length(min=2, max=255))
    created_date = fields.DateTime(dump_only=True, format='%d-%m-%Y %H:%M')

# class Photo(db.Model):
#     __tablename__ = 'photos'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255), nullable=False)
#     doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id', ondelete='CASCADE'), nullable=False)



user_schema = UserSchema()
user_login_schema = UserLoginSchema()
user_password_update_schema = UserPasswordUpdateSchema()
user_username_update_schema = UserUsernameUpdateSchema()
patient_schema = PatientSchema()
specialty_schema = SpecialtySchema()
doctor_schema = DoctorSchema()
hour_schema = HourSchema()
reception_schema = ReceptionSchema()
submission_schema = SubmissionSchema()
visit_schema = VisitSchema()

