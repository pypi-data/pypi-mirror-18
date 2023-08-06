def test_health_ping(app_client):
    response = app_client.get(app_client.url_for('health.ping'))
    assert response.status_code == 200
    assert response.text == 'OK'
    assert response.content_type == 'text/html; charset=utf-8'
