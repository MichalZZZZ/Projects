from flask import jsonify, abort
from clinic_app.utils import validate_json_content_type, token_required, get_schema_args, check_required_fields, apply_filter, apply_order, get_pagination
from webargs.flaskparser import use_args
from clinic_app.models import Submission, Patient, Doctor, Visit, VisitSchema
from clinic_app import db
from clinic_app.visits import visit_bp
from config import Config



config = Config()


@visit_bp.route('/show-all', methods=['GET'])
@token_required
def show_visits(user_id: int):
    query = db.session.query(Visit)
    schema_args = get_schema_args(Visit)
    query = apply_filter(Visit, query)
    query = apply_order(Visit, query)
    items, pagination = get_pagination(query, 'visits.show_visits')

    lists = VisitSchema(**schema_args).dump(items)

    return jsonify({
        'success': True,
        'visits': lists,
        'number_of_records': len(lists),
        'pagination': pagination
    }), 200


@visit_bp.route('/create/<int:submission_id>', methods=['POST'])
@token_required
@use_args(VisitSchema, error_status_code=400)
@validate_json_content_type
@check_required_fields(['recommendations', 'drugs', 'diagnosis'])
def create_visit(user_id: int, args: dict, submission_id: int):
    submission = db.session.query(Submission).filter(Submission.id == submission_id).first()
    doctor = db.session.query(Doctor).filter(Doctor.user_id == user_id).first()
    if submission is None:
        abort(404, description='Not found submission.')
    if doctor.id != submission.doctor_id:
        abort(403, description='You are not allowed to create a visit for this submission.')
    if submission.status != 'accepted':
        return jsonify({'message': 'The submission is pending or has been rejected.', 'success': False}), 400
    
    submission.status = 'visited'

    visit = Visit(**args)
    visit.submission_id = submission_id
    db.session.add(visit)
    db.session.commit()

    return jsonify({'message': 'Visit created.', 'success': True}), 201


@visit_bp.route('/show-all/me', methods=['GET'])
@token_required
def show_my_visits(user_id: int):
    patient = db.session.query(Patient).filter(Patient.user_id == user_id).first()
    if patient is None:
        return jsonify({'message': 'You dont have patient profile.', 'success': False}), 404
    else:
        schema_args = get_schema_args(Visit)
        schema_args['exclude'] = ['id', 'submission.patient']

        submissions = db.session.query(Submission).filter(Submission.patient_id == patient.id).all()
        submission_ids = [submission.id for submission in submissions]

        if len(submission_ids) == 0:
            abort(404, description='You dont have visits.')
        else:
            visits_query = db.session.query(Visit).filter(Visit.submission_id.in_(submission_ids))
            visits_query = apply_filter(Visit, visits_query)
            visits_query = apply_order(Visit, visits_query)
            visits, pagination = get_pagination(visits_query, 'visits.show_my_visits')
            visits_schema = VisitSchema(**schema_args)
            lists = visits_schema.dump(visits)

        return jsonify({
            'success': True,
            'visits': lists,
            'number_of_records': len(lists),
            'pagination': pagination
        }), 200
    

# testy
@visit_bp.route('/delete/<int:visit_id>', methods=['DELETE'])
@token_required
def delete_visit(user_id: int, visit_id: int):
    visit = db.session.query(Visit).filter(Visit.id == visit_id).first()
    if visit is None:
        abort(404, description=f'Visit on {visit_id} do not exists.')

    db.session.delete(visit)
    db.session.commit()

    return jsonify({'message': f'Visit {visit_id} has been deleted.', 'success': True}), 200