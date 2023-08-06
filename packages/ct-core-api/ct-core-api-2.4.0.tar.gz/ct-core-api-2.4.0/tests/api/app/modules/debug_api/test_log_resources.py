import logging

import pytest


@pytest.mark.parametrize(
    'level',
    map(logging.getLevelName, [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]))
def test_log_success(app_client, level):
    response = app_client.post(
        app_client.url_for('debug-api-v2.0.log_logging_resource'), data={'level': level, 'message': 'foo'})
    assert response.status_code == 204
    assert response.content_type == 'application/json'
