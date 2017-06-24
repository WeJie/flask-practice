from flask import jsonify

from . import api
from app.exceptions import ValidationError


def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return message

@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])

