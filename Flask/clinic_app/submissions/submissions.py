from flask import jsonify, abort
from clinic_app.utils import validate_json_content_type, token_required, get_schema_args, check_required_fields, apply_filter, apply_order, get_pagination
from webargs.flaskparser import use_args
from clinic_app.models import User, UserSchema, Submission, SubmissionSchema, submission_schema, Patient, PatientSchema, Hour, Doctor, CorrectnessSubmissionSchema, Visit
from clinic_app import db
from clinic_app.submissions import submission_bp
from datetime import datetime, timedelta
from config import Config
from flask_mail import Message
from clinic_app import mail

config = Config()


@submission_bp.route('/show-all', methods=['GET'])
@token_required
def show_submissions(user_id: int):
    query = db.session.query(Submission)
    schema_args = get_schema_args(Submission)
    query = apply_filter(Submission, query)
    query = apply_order(Submission, query)
    items, pagination = get_pagination(query, 'submissions.show_submissions')
    lists = SubmissionSchema(**schema_args).dump(items)

    return jsonify({
        'success': True,
        'submissions': lists,
        'number_of_records': len(lists),
        'pagination': pagination
    }), 200


@submission_bp.route('/show/<int:submission_id>', methods=['GET'])
@token_required
def show_single_submission(user_id: int, submission_id: int):
    submission = db.session.query(Submission).filter(Submission.id == submission_id).first()
    if submission is None:
        abort(404, description='Not found submission.')
    lists = SubmissionSchema().dump(submission)

    return jsonify({
        'success': True,
        'submission': lists
    }), 200


@submission_bp.route('/create', methods=['POST'])
@token_required
@use_args(SubmissionSchema, error_status_code=400)
@validate_json_content_type
@check_required_fields(['doctor_id', 'day', 'hour', 'medications_used', 'symptoms'])
def create_submission(user_id: int, args: dict):
    patient = db.session.query(Patient).filter(Patient.user_id == user_id).first()
    if patient is None:
        return jsonify({'message': 'You dont have patient profile.', 'success': False}), 404
    else:
        doctor = db.session.query(Doctor).filter(Doctor.id == args['doctor_id']).first()
        if doctor is None:
            return jsonify({'message': 'Doctor not found.', 'success': False}), 404

        appointment_datetime = datetime.combine(args['day'], args['hour'])
        now = datetime.now()
        minimum_allowed_datetime = datetime.now() + timedelta(hours=1)
        if appointment_datetime < minimum_allowed_datetime and appointment_datetime > now:
            return jsonify({'message': 'You must schedule the appointment at least 1 hours in advance.', 'success': False}), 400
        
        if appointment_datetime < now:
            return jsonify({'message': 'You cannot choose a past date or time.', 'success': False}), 400
        
        valid_hours = db.session.query(Hour).all()
        list_hours = []
        for hour in valid_hours:
            list_hours.append(hour.hour)

        str_hour = args['hour'].strftime('%H:%M')
        if str_hour not in list_hours:
            return jsonify({'message': f'Valid hours are: {list_hours}', 'success': False}), 400
        
        # patient_exists = db.session.query(Submission).filter(Submission.patient_id == patient.id, Submission.day == args['day']).first()
        # if patient_exists:
        #     return jsonify({'message': 'You already have a submission today.', 'success': 'False'}), 400

        submission = db.session.query(Submission).filter(Submission.day == args['day'], Submission.hour == args['hour'], Submission.doctor_id == doctor.id).first()
        if submission:
            if submission.status == 'accepted' or submission.status == 'waiting':
                return jsonify({'message': 'This term is already taken.', 'success': False}), 400
    
        args['patient_id'] = patient.id
        args['number'] = db.session.query(Submission).count() + 1
        submission = Submission(**args)
        db.session.add(submission)
        db.session.commit()

    return jsonify({'message': f'Submission created successfully.', 'success': True}), 201


@submission_bp.route('/show-all/me', methods=['GET'])
@token_required
def show_my_submissions(user_id: int):
    patient = db.session.query(Patient).filter(Patient.user_id == user_id).first()
    if patient is None:
        return jsonify({'message': 'You dont have patient profile.', 'success': False}), 404
    else:
        schema_args = get_schema_args(Submission)
        submissions = db.session.query(Submission).filter(Submission.patient_id == patient.id)
        # submission_schema = SubmissionSchema(**schema_args)
        submission_schema = SubmissionSchema(exclude=['patient'], **schema_args)
        submissions = apply_filter(Submission, submissions)
        submissions = apply_order(Submission, submissions)
        submissions, pagination = get_pagination(submissions, 'submissions.show_my_submissions')
        lists = submission_schema.dump(submissions)
        if len(lists) == 0:
            abort(404, description='You dont have submission.')

        return jsonify({
            'success': True,
            'submissions': lists,
            'number_of_records': len(lists),
            'pagination': pagination
        }), 200
    

@submission_bp.route('/cancel/<int:submission_id>', methods=['DELETE'])
@token_required
def cancel_submission(user_id: int, submission_id: int):
    patient = db.session.query(Patient).filter(Patient.user_id == user_id).first()
    submission = db.session.query(Submission).filter(Submission.id == submission_id).first()
    if submission is None:
        abort(404, description=f'Submission on {submission_id} do not exists.')

    if submission.patient_id != patient.id:
        abort(403, description=f'This submission does not belong to you.')

    formatted_datetime = datetime.now().strftime('%Y-%m-%d %H:%M')
    difference = datetime.combine(submission.day, submission.hour) - datetime.strptime(formatted_datetime, '%Y-%m-%d %H:%M')

    if difference.total_seconds() < 24 * 3600:
        return jsonify({'message': 'You cannot cancel your submission 24 hours in advance.', 'success': False}), 400
    db.session.delete(submission)
    db.session.commit()
    some_date = submission.hour.strftime('at: %H:%M')

    return jsonify({
        'success': True,
        'message': f'Your submission for {submission.day} {some_date} has been canceled.'
    }), 200


# poprawic testy
@submission_bp.route('/check-correctness/<int:submission_id>', methods=['POST'])
@token_required
@use_args(CorrectnessSubmissionSchema, error_status_code=400)
def check_correctness(user_id: int, args: dict, submission_id: int):
    submission = db.session.query(Submission).filter(Submission.id == submission_id).first()
    if submission is None:
        abort(404, description=f'Submission on {submission_id} do not exists.')
    patient = db.session.query(Patient).filter(Patient.id == submission.patient_id).first()
    date = datetime.combine(submission.day, submission.hour).strftime('%d-%m-%Y %H:%M')
    email_user = db.session.query(User).filter(User.id == patient.user_id).first()
    if submission.status == 'rejected' or submission.status == 'canceled':
        return jsonify({'message': 'This submission has already been considered.', 'success': False}), 400
    if submission.status == 'accepted': # test -----------
        if args['status'] != 'canceled': # test -----------
            return jsonify({'message': 'An accepted submission can only be canceled.', 'success': False}), 400

    submission.status = args['status']
    db.session.commit()

    subject = ''
    status = ''
    if args['status'] == 'rejected':
        subject = 'Submission rejected'
        status = 'rejected'
    if args['status'] == 'accepted':
        subject = 'Submission accepted'
        status = 'accepted'
    if args['status'] == 'canceled':
        subject = 'Submission canceled'
        status = 'canceled'

    msg = Message(subject=subject,
                recipients=[email_user.email],
                body=f'Hello {patient.first_name}. Your submission for the day {date} has been {status}. {args["message"]}')
    mail.send(msg)

    return jsonify({'message': f'The submission status has been changed to: {status}.', 'success': True}), 200


# testy
@submission_bp.route('/delete/<int:submission_id>', methods=['DELETE'])
@token_required
def delete_submission(user_id: int, submission_id: int):
    submission = db.session.query(Submission).filter(Submission.id == submission_id).first()
    if submission is None:
        abort(404, description=f'Submission on {submission_id} do not exists.')
    visit = db.session.query(Visit).filter(Visit.submission_id == submission_id).first()

    if visit is not None:
        db.session.delete(visit)
    db.session.delete(submission)
    db.session.commit()

    return jsonify({'message': f'Submission {submission_id} has been deleted.', 'success': True}), 200
