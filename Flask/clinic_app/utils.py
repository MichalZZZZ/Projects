from typing import List, Tuple
import jwt
from flask import jsonify, request, current_app, abort, url_for
from sqlalchemy import AliasedReturnsRows
from werkzeug.exceptions import UnsupportedMediaType
from functools import wraps
from flask_sqlalchemy.model import DefaultMeta
from clinic_app import db
import secrets
import re
from sqlalchemy.orm import Query
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.orm.attributes import InstrumentedAttribute
from clinic_app.models import Submission
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import joinedload


COMPARISON_OPERATORS_RE = re.compile(r'(.*)\[(gte|gt|lte|lt|==)\]')


def validate_json_content_type(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = request.get_json(silent=True)
        if data is None:
            raise UnsupportedMediaType('Content type must be application/json')
        return func(*args, **kwargs)
    return wrapper


def get_schema_args(model: DefaultMeta) -> dict:
    schema_args = {'many': True}
    fields = request.args.get('fields')
    if fields:
        schema_args['only'] = [field for field in fields.split(',') if field in model.__table__.columns]
    return schema_args


def apply_filter(model: DeclarativeMeta, query: Query) -> Query:
    for param, value in request.args.items():
        if param not in {'fields', 'sort', 'page', 'limit'}:
            operator = '=='
            match = COMPARISON_OPERATORS_RE.match(param)
            if match is not None:
                param, operator = match.groups()
            if 'submission.' in param:
                submission_column = param.split('.')[1]
                query = query.join(model.submission).filter(getattr(Submission, submission_column) == value)
            else:
                column_attr = getattr(model, param, None)
                if column_attr is not None:
                    value = model.additional_validation(param, value)
                    if value is None:
                        continue

                    filter_argument = _get_filter_argument(column_attr, value, operator)
                    query = query.filter(filter_argument)

    return query


def _get_filter_argument(column_name: InstrumentedAttribute, value: str, operator: str) -> BinaryExpression:
    operator_mapping = {
        '==': column_name == value,
        'gte': column_name >= value,
        'gt': column_name > value,
        'lte': column_name <= value,
        'lt': column_name < value
    }
    return operator_mapping[operator]


def apply_order(model: DefaultMeta, query: Query) -> Query:
    sort_keys = request.args.get('sort')
    if sort_keys:
        for key in sort_keys.split(','):
            desc = False
            if key.startswith('-'):
                key = key[1:]
                desc = True
            column_attr = getattr(model, key, None)
            if column_attr is not None:
                query = query.order_by(column_attr.desc()) if desc else query.order_by(column_attr)
    return query


def get_pagination(query: Query, func_name: str) -> Tuple[list, dict]:
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', current_app.config.get('PER_PAGE', 5), type=int)
    params = {key: value for key, value in request.args.items() if key != 'page'}
    paginate_obj = query.paginate(page=page, max_per_page=limit, error_out=False)
    pagination = {
        'total_pages': paginate_obj.pages,
        'total_record': paginate_obj.total,
        'current_page': url_for(func_name, page=page, **params)
    }

    if paginate_obj.has_next:
        pagination['next_page'] = url_for(func_name, page=page+1, **params)

    if paginate_obj.has_prev:
        pagination['previous_page'] = url_for(func_name, page=page-1, **params)

    return paginate_obj.items, pagination


permissions = {
    'patient': ['update_user_password', 'update_user_username', 'logout', 'delete_account', 'create_profile', 'get_profile', 'update_patient_phone_number', 'create_submission', 'get_hours_for_doctor_and_day', 'cancel_submission', 'show_my_submissions', 'show_my_visits', 'delete_patient_profile', 'show_user_profile'],
    'receptionist': ['check_correctness', 'show_single_submission', 'show_patient', 'show_doctor_card', 'get_hours_for_doctor_and_day', 'show_patients', 'show_submissions', 'show_visits', 'show_user_profile'],
    'doctor': ['show_single_submission', 'show_patient', 'create_visit', 'show_doctor_card', 'show_patients', 'show_submissions', 'show_visits', 'show_user_profile'],
    'admin': ['check_correctness', 'create_profile_doctor', 'add_admin', 'create_recepcjonist', 'delete_receptionist', 'delete_profile_doctor', 'register_user_function', 'get_users', 'show_patients', 'show_single_submission', 'show_doctor_card', 'get_hours_for_doctor_and_day', 'create_visit', 'create_submission', 'show_submissions', 'show_visits', 'show_user_profile', 'delete_user_function', 'delete_visit', 'delete_submission', 'logout']
}


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = None
        auth = request.headers.get('Authorization')
        if auth:
            token = auth.split(' ')[1]
        if token is None:
            abort(401, description='Missing token. Please login or register')
        try:
            payload = jwt.decode(token, current_app.config.get('SECRET_KEY'), algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            abort(401, description='Expired token. Please login or register')
        except jwt.InvalidTokenError:
            abort(401, description='Invalid token. Please login or register')
        else:
            user_id = payload['user_id']
            role = payload['role'] 
            if role not in permissions:
                abort(403, description='Unauthorized access')
            if func.__name__ not in permissions[role]:
                abort(403, description='Unauthorized access')
            return func(user_id, *args, **kwargs)
    return wrapper


def decode_token(token):
    decoded_token = jwt.decode(token, current_app.config.get('SECRET_KEY'), algorithms=['HS256'])
    return decoded_token


def check_required_fields(required_fields):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            args_dict = request.get_json() or {}
            for field in required_fields:
                if field not in args_dict:
                    return jsonify({'message': f'{field} is required.', 'success': False}), 400
                if isinstance(args_dict[field], str) and not args_dict[field].strip():
                    return jsonify({'message': f'{field} is required.', 'success': False}), 400
            return func(*args, **kwargs)
        return wrapped
    return decorator


def generate_reset_token():
    return secrets.token_urlsafe(32)


def generate_reset_password_link(email, token):
    reset_link = f'http://your-app-url/reset-password/{email}/{token}'
    return reset_link


