from flask_restplus.errors import abort as restplus_abort
from werkzeug.exceptions import Conflict, Forbidden, NotFound, Unauthorized, UnprocessableEntity

from ct_core_api.api.lib.flask_restplus._http import HTTPStatus  # noqa


API_DEFAULT_HTTP_CODE_MESSAGES = {
    Unauthorized.code: Unauthorized.description,
    Forbidden.code: Forbidden.description,
    NotFound.code: NotFound.description,
    Conflict.code: Conflict.description,
    UnprocessableEntity.code: UnprocessableEntity.description}


def abort(code, message=None, **kwargs):
    if message is None:
        message = API_DEFAULT_HTTP_CODE_MESSAGES.get(code)
    restplus_abort(code=code, status=code, message=message, **kwargs)
