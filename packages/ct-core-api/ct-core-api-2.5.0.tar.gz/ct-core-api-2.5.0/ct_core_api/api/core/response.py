from flask_restplus.errors import abort as restplus_abort
from werkzeug.exceptions import Conflict, Forbidden, NotFound, Unauthorized, UnprocessableEntity

from ct_core_api.api.core.schema import APISchema
from ct_core_api.api.lib.flask_restplus._http import HTTPStatus  # noqa
from ct_core_api.api.lib.flask_restplus.response import HTTPErrorSchema

HTTPStatus = HTTPStatus


class APIErrorSchema(HTTPErrorSchema, APISchema):
    # TODO: Introduce an `error_code` EnumField to provide application-level error codes using an `APIError` Enum
    # TODO: Introduce a `params` field to provide details on which input(s) are invalid
    pass


API_DEFAULT_HTTP_CODE_MESSAGES = {
    Unauthorized.code: Unauthorized.name,
    Forbidden.code: Forbidden.name,
    NotFound.code: NotFound.name,
    Conflict.code: Conflict.name,
    UnprocessableEntity.code: UnprocessableEntity.name}


def abort(code, message=None, **kwargs):
    if message is None:
        message = API_DEFAULT_HTTP_CODE_MESSAGES.get(code)
    restplus_abort(code=code, status=code, message=message, **kwargs)


def generate_api_error_response(message, status_code, error_code=None, params=None, headers=None):
    error_data = dict(message=message)

    if error_code is not None:
        error_data['error_code'] = error_code

    if params is not None:
        error_data['params'] = error_code

    error_schema = APIErrorSchema(status_code)
    data = error_schema.dump(error_data).data
    if headers:
        return data, status_code, headers
    return data, status_code
