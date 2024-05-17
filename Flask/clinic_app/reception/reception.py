from flask import jsonify, abort
from clinic_app.utils import validate_json_content_type, token_required, get_schema_args, check_required_fields
from webargs.flaskparser import use_args
from clinic_app.models import User, Reception, ReceptionSchema, reception_schema, Patient
from clinic_app import db
from clinic_app.reception import reception_bp


@reception_bp.route('/show-all', methods=['GET'])
def show_reception():
    schema_args = get_schema_args(Reception)
    receptions = db.session.query(Reception).all()
    reception_schema = ReceptionSchema(**schema_args)
    lists = reception_schema.dump(receptions)

    return jsonify({
        'receptionists': lists,
        'success': True,
    }), 200


@validate_json_content_type
@reception_bp.route('/create', methods=['POST'])
@check_required_fields(['name', 'last_name', 'user_id'])
@token_required
@use_args(ReceptionSchema, error_status_code=400)
def create_recepcjonist(user_id: int, args: dict):
    role = db.session.query(User).filter(User.role == 'receptionist', User.id == args['user_id']).first()
    exists_reception = db.session.query(Reception).filter(Reception.user_id == args['user_id']).first()
    existing_user = db.session.query(User).filter(User.id == args['user_id']).first()

    if existing_user is None: 
        abort(404, description='Not found user.') 
    elif role is None:
        abort(403, description='This user does not have permission to use this function.') 
    elif exists_reception is not None:
        abort(409, description='This user have a receptionist profile.') 
    else:
        if db.session.query(Reception).filter(Reception.phone_number == args['phone_number']).first(): 
            abort(409, description='Phone number already exists.')
        if db.session.query(Patient).filter(Patient.phone_number == args['phone_number']).first(): 
            abort(409, description='Phone number already exists.') 

        reception = Reception(**args) 

        db.session.add(reception) 
        db.session.commit() 

        return jsonify({
            'success': True,
            'message': 'Receptionist profile created successfully.'
        }), 201
    

# testy do tego
@reception_bp.route('/delete-profile/<int:user_id>', methods=['DELETE'])
@token_required
def delete_receptionist(reception_id: int, user_id: int):
    reception = db.session.query(Reception).filter(Reception.id == user_id).first()
    if reception is None:
        abort(404, description='Not found receptionist profile.')
    else:
        user = db.session.query(User).filter(User.id == reception.user_id).first()
        db.session.delete(reception)
        db.session.delete(user)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Receptionist profile deleted successfully.'
        }), 200