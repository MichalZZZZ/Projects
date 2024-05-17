from datetime import datetime
from flask import request, jsonify, abort
from clinic_app.utils import validate_json_content_type, token_required, get_schema_args, check_required_fields, apply_filter, apply_order, get_pagination
from webargs.flaskparser import use_args
from clinic_app.models import User, Doctor, DoctorSchema, Specialty, doctor_schema, Hour, Submission, SubmissionSchema, Visit
from clinic_app import db
from clinic_app.doctors import doctor_bp
from datetime import datetime
from sqlalchemy import and_, func, or_
from sqlalchemy.orm import aliased


@doctor_bp.route('/show-all', methods=['GET'])
def show_doctors():
    query = db.session.query(Doctor)
    schema_args = get_schema_args(Doctor)
    query = apply_filter(Doctor, query)
    query = apply_order(Doctor, query)
    items, pagination = get_pagination(query, 'doctors.show_doctors')
    lists = DoctorSchema(**schema_args).dump(items)

    return jsonify({
        'success': True,
        'doctors': lists,
        'number_of_records': len(lists),
        'pagination': pagination
    }), 200


@doctor_bp.route('/show-one/<int:doctor_id>', methods=['GET'])
def show_doctor_for_patient(doctor_id: int):
    doctor = db.session.query(Doctor).filter(Doctor.id == doctor_id).first()
    if doctor is None:
        abort(404, description='Not found.')
    data_doctor = doctor_schema.dump(doctor)

    return jsonify({
        'doctor': data_doctor,
        'success': True
    })



@doctor_bp.route('/show-card/<int:doctor_id>', methods=['GET'])
@token_required
def show_doctor_card(user_id: int, doctor_id: int):
    doctor = db.session.query(Doctor).filter(Doctor.id == doctor_id).first()
    if doctor is None:
        abort(404, description='Not found doctor.')
    data_doctor = DoctorSchema(exclude=['description']).dump(doctor)

    submissions = db.session.query(Submission).filter((Submission.doctor_id == doctor.id) & (or_(Submission.status == 'waiting', Submission.status == 'accepted')))
    schema_args = get_schema_args(Submission)
    schema_args['exclude'] = ['doctor', 'patient.address', 'patient.first_name', 'patient.last_name', 'patient.phone_number']
    submission_schema = SubmissionSchema(**schema_args)
    submissions = apply_filter(Submission, submissions)
    submissions = apply_order(Submission, submissions)
    # submissions, pagination = get_pagination(submissions, 'submissions.show_submissions')

    return jsonify({
        'doctor': data_doctor,
        'submissions': submission_schema.dump(submissions),
        # 'number_of_records': len(submission_schema.dump(submissions)),
        # 'pagination': pagination,
        'success': True
    })


@doctor_bp.route('/create-profile', methods=['POST'])
@validate_json_content_type
@token_required
@check_required_fields(['name', 'last_name', 'seniority', 'description', 'specialty_id', 'photo', 'user_id'])
@use_args(DoctorSchema, error_status_code=400)
def create_profile_doctor(user_id: int, args: dict):
    role = db.session.query(User).filter(User.role == 'doctor', User.id == args['user_id']).first()
    exists_doctor = db.session.query(Doctor).filter(Doctor.user_id == args['user_id']).first()
    specialty = db.session.query(Specialty).filter(Specialty.id == args['specialty_id']).first()
    existing_user = db.session.query(User).filter(User.id == args['user_id']).first()

    if existing_user is None:
        abort(404, description='Not found user.')
    if role is None:
        abort(403, description='This user does not have permission to use this function.')
    if specialty is None:
        abort(404, description='Not found specialty.')
    if exists_doctor is not None:
        abort(409, description='This user is doctor.')

    args['photo'] = 'assets/images/' + args['photo']
    doctor = Doctor(**args)
    db.session.add(doctor)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Profile doctor created successfully.'
    }), 201


@doctor_bp.route('/hours/<int:doctor_id>/<string:date>', methods=['GET'])
@token_required
def get_hours_for_doctor_and_day(user_id: int, doctor_id: int, date: str):
    datex = datetime.strptime(date, '%d-%m-%Y').date()
    now = datetime.now().date()
    if datex < now:
        return jsonify({'message': 'There is no such day.', 'success': False }), 400
    doctor = db.session.query(Doctor).filter(Doctor.id == doctor_id).first()
    if doctor is None:
        abort(404, description='Not found doctor.')
    lists = db.session.query(Submission).filter(Submission.doctor_id == doctor_id, func.DATE(Submission.day) == datex, Submission.status != 'rejected', Submission.status != 'visited').all()
    lists2 = db.session.query(Hour).all()
    hours_busy = [submission.hour for submission in lists]
    hours_busy_strings = [hour.strftime("%H:%M") for hour in hours_busy]
    hours_available = [hour.hour for hour in lists2]
    hours_unavailable = [i for i in hours_available if i not in hours_busy_strings]
    doctor_schema = DoctorSchema(exclude=['photo', 'description', 'seniority'])
    lists2 = doctor_schema.dump(doctor)
    return jsonify({
        'doctor': lists2,
        'hours_available': hours_unavailable,
        'success': True
    }), 200


# testy
@doctor_bp.route('/delete-profile/<int:doctor_id>', methods=['DELETE'])
@token_required
def delete_profile_doctor(user_id: int, doctor_id: int):
    doctor = db.session.query(Doctor).filter(Doctor.id == doctor_id).first()
    if doctor is None:
        abort(404, description='Not found doctor.')
    user = db.session.query(User).filter(User.id == doctor.user_id).first()
    submissions = db.session.query(Submission).filter(Submission.doctor_id == doctor.id).all()
    visits = db.session.query(Visit).all()
    submission_id = []
    for sub in submissions:
        submission_id.append(sub.id)
    for visit in visits:
        if visit.submission_id in submission_id:
            db.session.delete(visit)
    for submission in submissions:
        db.session.delete(submission)
    db.session.delete(doctor)
    db.session.delete(user)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Profile doctor deleted successfully.'
    }), 200