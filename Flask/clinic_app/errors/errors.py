from flask import Response, jsonify
from clinic_app.errors import errors_bp


class ErrorResponse:
    def __init__(self, message: str, http_status: int):
        self.payload = {
            'success': False,
            'message': message
        }
        self.http_status = http_status

    def to_response(self) -> Response:
        response = jsonify(self.payload)
        response.status_code = self.http_status
        return response


@errors_bp.app_errorhandler(400)
def bad_request_error(err):
    messages = err.data.get('messages', {}).get('json', {})
    return ErrorResponse(messages, 400).to_response()


@errors_bp.app_errorhandler(401)
def not_found_error(err):
    return ErrorResponse(err.description, 401).to_response()


@errors_bp.app_errorhandler(403)
def unauthorized_error(err):
    return ErrorResponse(err.description, 403).to_response()


@errors_bp.app_errorhandler(404)
def not_found_error(err):
    return ErrorResponse(err.description, 404).to_response()


@errors_bp.app_errorhandler(409)
def unsupported_media_type_error(err):
    return ErrorResponse(err.description, 409).to_response()