from flask import request, jsonify, abort
from clinic_app.utils import validate_json_content_type, check_required_fields, token_required
from webargs.flaskparser import use_args
from clinic_app.models import user_schema, User
from clinic_app.admin import admin_bp
from werkzeug.security import generate_password_hash
from config import Config
from clinic_app import db


config_2 = Config()


@admin_bp.route('/add', methods=['POST'])
@validate_json_content_type
@check_required_fields(['username', 'password'])
def add_admin():
    args = request.get_json()
    if db.session.query(User).filter(User.username == args['username']).first():
        abort(409, 'Username already exists.')
    if db.session.query(User).filter(User.email == args['email']).first():
        abort(409, 'Email already exists.')
        
    args['role'] = 'admin'
    if args['password'] != args['confirm_password'] or args['confirm_password'] != args['password']:
        return jsonify({'message': 'Passwords do not match.', 'success': False}), 400
    args['password'] = generate_password_hash(args['password'])

    args.pop('confirm_password', None)

    user = User(**args)

    db.session.add(user)
    db.session.commit()
    token = user.generate_jwt()

    response_data = {
        'success': True,
        'message': 'User created successfully.',
        'token': token
    }
    return jsonify(response_data), 201
