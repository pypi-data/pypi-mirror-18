import pytest


def _tc_params(exception_cls, expected_status_code, expected_content):
    expected_content.setdefault('status_code', expected_status_code)
    return exception_cls, expected_status_code, expected_content


@pytest.mark.parametrize('exception_cls, expected_status_code, expected_content', [
    _tc_params('flask_principal.PermissionDenied', 403, {'message': 'Forbidden'}),
    _tc_params('sqlalchemy.orm.exc.NoResultFound', 404, {'message': 'Not Found'}),
    _tc_params('validation21.ValidationException', 422, {'message': 'Unprocessable Entity'})])
def test_config_get_success(app_client, exception_cls, expected_status_code, expected_content):
    response = app_client.post(
        app_client.url_for('debug-api-v2.0.error_error_exception_resource'),
        data={'exception_cls': exception_cls})
    assert response.content_type == 'application/json'
    assert response.status_code == expected_status_code
    assert response.json == expected_content
