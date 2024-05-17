from datetime import datetime
from flask import jsonify, abort
from clinic_app.utils import validate_json_content_type, token_required, get_schema_args, check_required_fields, apply_filter, apply_order, get_pagination
from webargs.flaskparser import use_args
from clinic_app.models import Patient, PatientSchema, User, PhoneNumberUpdate, Submission, Visit, SubmissionSchema, VisitSchema, UserPasswordAuthorizationSchema, Reception
from clinic_app import db
from clinic_app.patients import patient_bp
import pesel_utils


# poprawic testy do tego
@patient_bp.route('/show-all', methods=['GET'])
@token_required
def show_patients(user_id: int):
    query = db.session.query(Patient)
    schema_args = get_schema_args(Patient)
    query = apply_filter(Patient, query)
    query = apply_order(Patient, query)
    items, pagination = get_pagination(query, 'patients.show_patients')
    lists = PatientSchema(**schema_args).dump(items)

    return jsonify({
        'success': True,
        'patients': lists,
        'number_of_records': len(lists),
        'pagination': pagination
    }), 200


@patient_bp.route('/show-one/<int:patient_id>', methods=['GET'])
@token_required
def show_patient(user_id: int, patient_id: int):
    patient = db.session.query(Patient).filter(Patient.id == patient_id).first()
    if patient is None:
        abort(404, description='Not found patient.')

    submissions = db.session.query(Submission).filter(Submission.patient_id == patient.id).all()
    lists = PatientSchema().dump(patient)
    schema_args_visit = get_schema_args(Visit)
    schema_args_visit['exclude'] = ['id', 'submission.patient']

    visits = []
    for submission in submissions:
            visit = db.session.query(Visit).filter(Visit.submission_id == submission.id).first()
            if visit:
                visits.append(visit)

    visits_schema = VisitSchema(**schema_args_visit)

    return jsonify({
        'patient': lists,
        'treatment_history': visits_schema.dump(visits),
        'success': True,
    }), 200


@patient_bp.route('/create', methods=['POST'])
@validate_json_content_type
@token_required
@check_required_fields(['first_name', 'last_name', 'address'])
@use_args(PatientSchema, error_status_code=400)
def create_profile(user_id: int, args: dict):
    check = db.session.query(Patient).filter(Patient.pesel == args['pesel']).first()
    # user = db.session.query(User).filter(User.id == user_id).first() # dodac testy do tego
    # if user is None:
    #     abort(404, description='Not found user.')
    if check is not None:
        abort(409, description='This PESEL is already linked to the account.')
    else:
        if db.session.query(Patient).filter(Patient.phone_number == args['phone_number']).first():
            abort(409, 'Phone number already exists.')
        elif pesel_utils.is_valid(args['pesel']) is False:
            return jsonify({'message': 'Invalid pesel.', 'success': 'False'}), 400
        elif db.session.query(Reception).filter(Reception.phone_number == args['phone_number']).first():
            abort(409, 'Phone number already exists.')
        
    birthdate_string = pesel_utils.check_birthdate(args['pesel'])
    parts = birthdate_string.split('/')
    year = int(parts[0])
    month = int(parts[1])
    day = int(parts[2])

    date_of_birth = datetime(year, month, day).date()
    args['date_of_birth'] = date_of_birth
    args['user_id'] = user_id
    user = Patient(**args)

    db.session.add(user)
    db.session.commit()

    response_data = {
        'message': 'Profile created successfully.',
        'success': True
    }
    return jsonify(response_data), 201


@patient_bp.route('/profile-me', methods=['GET'])
@token_required
def get_profile(user_id: int):
    patient = db.session.query(Patient).filter(Patient.user_id == user_id).first()
    if not patient:
        abort(404, description="You don't have a patient profile.")
        
    patient_schema = PatientSchema()

    return jsonify({
        'patient': patient_schema.dump(patient),
        'success': True,
    }), 200


@patient_bp.route('/update-phone', methods=['PATCH'])
@use_args(PhoneNumberUpdate, error_status_code=400)
@token_required
def update_patient_phone_number(user_id: int, args: dict):
    patient = db.session.query(Patient).filter(Patient.user_id == user_id).first()
    if not patient:
        abort(404, description="You don't have a patient profile.")
    if db.session.query(Patient).filter(Patient.phone_number == args['phone_number']).first():
        abort(409, description='This phone number already exists.')

    patient.phone_number = args['phone_number']
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Your phone number has been updated.'
    }), 200

    
# poprawic testy do tego
@patient_bp.route('/delete-profile', methods=['DELETE'])
@token_required
@use_args(UserPasswordAuthorizationSchema, error_status_code=400)
def delete_patient_profile(user_id: int, args: dict):
    patient = db.session.query(Patient).filter(Patient.user_id == user_id).first()
    if patient is None:
        abort(404, description='You dont have patient profile.')
    else:
        user = db.session.query(User).filter(User.id == user_id).first()
        submissions = db.session.query(Submission).filter(Submission.patient_id == patient.id).all()
        visits = db.session.query(Visit).all()
        submission_id = []
        for sub in submissions:
            submission_id.append(sub.id)
        for visit in visits:
            if visit.submission_id in submission_id:
                db.session.delete(visit)
        for submission in submissions:
            db.session.delete(submission)
        if not user.is_password_valid(args['password']):
            return jsonify({'message': 'Bad password.', 'success': False}), 400
        if args['password'] != args['confirm_password']:
            return jsonify({'message': 'Passwords do not match.', 'success': False}), 400
        db.session.delete(patient)
        db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Your profile has been deleted.'
    }), 200