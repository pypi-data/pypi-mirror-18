import json

from jsonschema import RefResolver
from swagger_spec_validator import validator20


def test_openapi_spec_validity(app_client):
    raw_openapi_spec = app_client.get(app_client.url_for('debug-api-v1.specs')).data
    deserialized_openapi_spec = json.loads(raw_openapi_spec.decode('utf-8'))
    assert isinstance(validator20.validate_spec(deserialized_openapi_spec), RefResolver)
