def test_config_get_success(app_client, app):
    response = app_client.get(app_client.url_for('debug-api-v2.0.config_app_config_resource'))
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert set(response.json.keys()) == set(app.config.keys())
