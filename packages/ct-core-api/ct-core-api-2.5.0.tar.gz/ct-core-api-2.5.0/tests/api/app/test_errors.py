import pytest
from flask_principal import PermissionDenied
from sqlalchemy.orm.exc import NoResultFound
from validation21 import ValidationException
from werkzeug.exceptions import HTTPException

from tests.utils import ah


class _UnknownException(Exception):
    pass


class _CustomPermissionDenied(PermissionDenied):
    pass


class _CustomHTTPException(HTTPException):
    pass


def _tc_params(exception_cls, expected_status_code, expected_content, *exception_args, **exception_data):
    expected_content.setdefault('status_code', expected_status_code)
    return exception_cls, exception_args, exception_data, expected_status_code, expected_content


@pytest.mark.parametrize('exception_cls, exception_args, exception_data, expected_status_code, expected_content', [
    # 403 Exceptions
    _tc_params(PermissionDenied, 403, {'message': 'Forbidden'}),
    _tc_params(PermissionDenied, 403, {'message': 'Forbidden'}, 'A'),
    _tc_params(PermissionDenied, 403, {'message': 'B'}, 'A', message='B'),
    _tc_params(_CustomPermissionDenied, 403, {'message': 'Forbidden'}),
    _tc_params(_CustomPermissionDenied, 403, {'message': 'Forbidden'}, 'A'),
    _tc_params(_CustomPermissionDenied, 403, {'message': 'B'}, 'A', message='B'),

    # 404 Exceptions
    _tc_params(NoResultFound, 404, {'message': 'Not Found'}),
    _tc_params(NoResultFound, 404, {'message': 'Not Found'}, 'A'),
    _tc_params(NoResultFound, 404, {'message': 'B'}, 'A', message='B'),

    # 422 Exceptions
    _tc_params(ValidationException, 422, {'message': 'Unprocessable Entity'}),

    # 500 Exceptions
    _tc_params(_UnknownException, 500, {'message': 'Internal Server Error'})])
def test_api_error_handlers(
        app, core_api, exception_cls, exception_args, exception_data, expected_status_code, expected_content):
    with pytest.raises(exception_cls) as exc_info:
        raise exception_cls(*exception_args)
    exc = exc_info.value
    exc.data = exception_data

    with app.test_request_context('/'):
        resp = core_api.handle_error(exc)
        assert resp.content_type == 'application/json'
        assert resp.status_code == expected_status_code
        json_content = ah.extract_response_json(resp)
        assert json_content == expected_content
