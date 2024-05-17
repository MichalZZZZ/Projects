from flask import request, jsonify, abort
from clinic_app.utils import validate_json_content_type, token_required, get_schema_args, check_required_fields, generate_reset_token, generate_reset_password_link, apply_filter, apply_order, get_pagination
from webargs.flaskparser import use_args
from clinic_app.models import user_schema, User, UserSchema, UserLoginSchema, UserPasswordUpdateSchema, user_password_update_schema, user_username_update_schema, Token, TokenSetPassword, Patient, Reception, Doctor
from clinic_app import db, mail
from clinic_app.auth import auth_bp
from werkzeug.security import generate_password_hash
from flask_mail import Message
from config import Config


config_2 = Config()


# testy
@auth_bp.route('/show-user-profile', methods=['GET'])
@token_required
def show_user_profile(user_id: int):
    user = db.session.query(User).filter(User.id == user_id).first()
    if user is None:
        abort(404, description='User not found.')
    user_schema = UserSchema()
    user_data = user_schema.dump(user)
    return jsonify({'success': True, 'user': user_data}), 200
        


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data.get('email')
    login2 = db.session.query(User).filter_by(email=email).first()

    if not email.strip():
        return jsonify({'message': 'Please enter your email address.', 'success': False}), 400

    if login2 is None:
        abort(404, description='This email is not associated with any account.')

    token = generate_reset_token()
    reset_link = generate_reset_password_link(email, token)

    msg = Message(subject='Reset password',
                  recipients=[email],
                  body=f'Hello, click the following link to reset your password: {reset_link}')
    mail.send(msg)

    check_send_reset = db.session.query(TokenSetPassword).filter_by(email=email).first()
    if check_send_reset:
        abort(409, description='You have already sent a password reset link. Please check your email.')
        
    new_token = TokenSetPassword(token=token, email=email, user_id=login2.id)
    db.session.add(new_token)
    db.session.commit()

    return jsonify({'message': 'We have sent a password reset link to your email.', 'success': True}), 200
     

@auth_bp.route('/reset-password/<email>/<token>', methods=['POST'])
@validate_json_content_type
@check_required_fields(['password', 'confirm_password'])
def reset_password_submit(email, token):
    check_token = db.session.query(TokenSetPassword).filter_by(token=token).first()
    data = request.get_json()
    if check_token:
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            return jsonify({'message': 'Passwords do not match.', 'success': False}), 400

        user = db.session.query(User).filter_by(email=email).first()

        if user:
            user.password = generate_password_hash(password)
            delete_token = db.session.query(TokenSetPassword).filter_by(token=token).first()
            db.session.delete(delete_token)
            db.session.commit()
        else:
            return jsonify({'message': 'Invalid email.', 'success': False}), 400
    else:
        return jsonify({'message': 'Invalid or expired reset link.', 'success': False}), 400

    return jsonify({'message': 'Password has been changed successfully.', 'success': True}), 200


@auth_bp.route('/contact', methods=['POST'])
def contact():
    data = request.get_json()
    email = data.get('email')
    message = data.get('message')
    subject = data.get('subject')

    if not email.strip():
        return jsonify({'message': 'Please enter your email address.', 'success': False}), 400
    if not message.strip():
        return jsonify({'message': 'Please enter your message.', 'success': False}), 400
    if not subject.strip():
        return jsonify({'message': 'Please enter your subject.', 'success': False}), 400

    msg = Message(subject=f'{subject} - od: {email}',
        recipients=[config_2.MAIL_USERNAME],
        body=f'You have received a message from {email}. Message: {message}')
    mail.send(msg)

    return jsonify({'message': 'Your message has been sent.', 'success': True}), 200


@auth_bp.route('/users', methods=['GET'])
@token_required
def get_users(user_id: int):
    query = db.session.query(User)
    schema_args = get_schema_args(User)
    query = apply_filter(User, query)
    query = apply_order(User, query)
    items, pagination = get_pagination(query, 'auth.get_users')
    lists = UserSchema(exclude=['password'], **schema_args).dump(items)

    return jsonify({
        'success': True,
        'users': lists,
        'number_of_records': len(lists),
        'pagination': pagination
    }), 200


@auth_bp.route('/register', methods=['POST'])
@validate_json_content_type
@check_required_fields(['username', 'password', 'confirm_password', 'email'])
def register():
    args = request.get_json()
    if db.session.query(User).filter(User.username == args['username']).first():
        abort(409, 'Username already exists.')
    if db.session.query(User).filter(User.email == args['email']).first():
        abort(409, 'Email already exists.')
    if '@' not in args['email']:
        return jsonify({'message': 'Invalid email format.', 'success': False}), 400
    if len(args['password']) < 6:
        return jsonify({'message': 'Password must be at least 6 characters.', 'success': False}), 400
        
    args['role'] = 'patient'

    if args['password'] != args['confirm_password'] or args['confirm_password'] != args['password']:
        return jsonify({'message': 'Passwords do not match.', 'success': False}), 400
    args['password'] = generate_password_hash(args['password'])

    args.pop('confirm_password', None)

    user = User(**args)

    db.session.add(user)
    db.session.commit()
    token = user.generate_jwt()

    msg = Message(subject='Registration',
                  recipients=[args['email']],
                  body=f'Hello. Thank you for your registration in our clinic.')
    mail.send(msg)

    response_data = {
        'success': True,
        'message': 'User created successfully.',
        'token': token
    }
    return jsonify(response_data), 201


@auth_bp.route('/login', methods=['POST'])
@use_args(UserLoginSchema, error_status_code=400)
def login(args: dict):
    user = db.session.query(User).filter(User.username == args['username']).first()

    if not user:
        abort(401, description='Invalid username or password.')

    if not user.is_password_valid(args['password']):
        abort(401, description='Invalid username or password.')

    already = db.session.query(Token).filter(Token.user_id == user.id).first()
    if already:
        abort(401, description='You are already logged in.')
    else:
        token = user.generate_jwt()
        token_with_bearer = 'Bearer ' + token
        new_token = Token(token=token_with_bearer, user_id=user.id)
        db.session.add(new_token)
        db.session.commit()

        if request.method == 'POST':
            return jsonify({
                'success': True,
                'token': token
            }), 200
    

@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout(token):
    token = request.headers.get('Authorization')
    user_token = db.session.query(Token).filter_by(token=token).first()
    if user_token:
        db.session.delete(user_token)
        db.session.commit()
        return jsonify({'message': 'Logged out successfully.', 'success': 'True'}), 200
    else:
        abort(401, description='Your session has expired.')


@auth_bp.route('/update-password', methods=['PUT'])
@token_required
@check_required_fields(['current_password', 'new_password', 'confirm_new_password'])
@use_args(user_password_update_schema, error_status_code=400)
def update_user_password(user_id: int, args: dict):
    user = db.session.query(User).filter(User.id == user_id).first()

    if not user.is_password_valid(args['current_password']):
        return jsonify({'message': 'Bad password.', 'success': False}), 400
    if args['current_password'] == args['new_password']:
        return jsonify({'message': 'Do not use the same password.', 'success': False}), 400
    if args['new_password'] != args['confirm_new_password']:
        return jsonify({'message': 'Passwords do not match.', 'success': False}), 400

    user.password = user.generate_hashed_password(args['new_password'])
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Password has been updated successfully.'
    }), 200


@auth_bp.route('/update-username', methods=['PUT'])
@token_required
@check_required_fields(['new_username', 'password'])
@use_args(user_username_update_schema, error_status_code=400)
def update_user_username(user_id: int, args: dict):
    user = db.session.query(User).filter(User.id == user_id).first()

    if not user.is_password_valid(args['password']):
        return jsonify({'message': 'Bad password.', 'success': False}), 400
    else:
        if user.username == args['new_username']:
            abort(409, description='Username already exists.')
        else:
            user.username = args['new_username']

    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Username has been updated successfully.'
    }), 200


@auth_bp.route('/delete-account', methods=['DELETE'])
@token_required
def delete_account(user_id: int):
    patient = db.session.query(Patient).filter(Patient.user_id == user_id).first()
    if patient:
        abort(409, description='You have a patient profile. Please delete it first.')
    data = request.get_json()
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    user = db.session.query(User).filter(User.id == user_id).first()
    token = request.headers.get('Authorization')
    user_token = db.session.query(Token).filter_by(token=token).first()

    if not user.is_password_valid(password):
        return jsonify({'message': 'Bad password.', 'success': False}), 400
    if password != confirm_password:
        return jsonify({'message': 'Passwords do not match.', 'success': False}), 400

    db.session.delete(user_token)
    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'Account has been deleted successfully.', 'success': True}), 200




# testy
@auth_bp.route('/add-user-function', methods=['POST'])
@token_required
@validate_json_content_type
@check_required_fields(['username', 'password', 'confirm_password', 'email', 'role'])
def register_user_function(user_id: int):
    args = request.get_json()
    if db.session.query(User).filter(User.username == args['username']).first():
        abort(409, 'Username already exists.')
    if db.session.query(User).filter(User.email == args['email']).first():
        abort(409, 'Email already exists.')
    if '@' not in args['email']:
        return jsonify({'message': 'Invalid email format.', 'success': False}), 400
    if len(args['password']) < 6:
        return jsonify({'message': 'Password must be at least 6 characters.', 'success': False}), 400
    if args['role'] != 'receptionist' and args['role'] != 'admin' and args['role'] != 'doctor':
        abort(403, description='The available roles are: [doctor, admin, receptionist.]')
        
    if args['password'] != args['confirm_password'] or args['confirm_password'] != args['password']:
        return jsonify({'message': 'Passwords do not match.', 'success': False}), 400
    args['password'] = generate_password_hash(args['password'])

    args.pop('confirm_password', None)

    user = User(**args)

    db.session.add(user)
    db.session.commit()
    user_id = user.id

    response_data = {
        'success': True,
        'message': f'User with role {args["role"]} created successfully.',
        'ID': f'User id: {user_id}'
    }
    return jsonify(response_data), 201


# testy
@auth_bp.route('/delete-user-function/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user_function(admin_id: int, user_id: int):
    user = db.session.query(User).filter(User.id == user_id).first()
    reception = db.session.query(Reception).filter(Reception.user_id == user_id).first()
    doctor = db.session.query(Doctor).filter(Doctor.user_id == user_id).first()
    all_admin = db.session.query(User).filter(User.role == 'admin').all()

    if user is None:
        abort(404, description='Not found user.')
    if reception is not None:
        abort(409, description='This user has a function receptionist. Please delete receptionist.')
    if doctor is not None:
        abort(409, description='This user has a function doctor. Please delete doctor.')
    if user.role == 'patient':
        abort(403, description='You cannot delete a patient profile.')
    if len(all_admin) == 1 and user.role == 'admin':
        abort(403, description='You cannot delete the last admin profile.')
    db.session.delete(user)
    db.session.commit()
    return jsonify({
        'success': True,
        'message': 'User deleted successfully.'
    }), 200