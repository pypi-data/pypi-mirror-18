import json

from flask import Response, url_for
from flask.testing import FlaskClient
from jsonschema import RefResolver
from swagger_spec_validator import validator20
from werkzeug.utils import cached_property


class AppResponse(Response):
    @cached_property
    def text(self):
        return self.get_data(as_text=True)

    @cached_property
    def json(self):
        return json.loads(self.text)


class AppClient(FlaskClient):
    def url_for(self, endpoint, **values):
        with self.application.test_request_context('/'):
            return url_for(endpoint, **values)


def validate_openapi_spec(app_client, spec_endpoint):
    deserialized_openapi_spec = app_client.get(app_client.url_for(spec_endpoint)).json
    assert isinstance(validator20.validate_spec(deserialized_openapi_spec), RefResolver)
