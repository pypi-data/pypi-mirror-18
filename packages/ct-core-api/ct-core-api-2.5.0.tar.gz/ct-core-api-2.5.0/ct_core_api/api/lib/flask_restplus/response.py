import flask_marshmallow

from .schema import Schema


class HTTPErrorSchema(Schema):
    status_code = flask_marshmallow.base_fields.Integer(required=True)
    message = flask_marshmallow.base_fields.String()

    def __init__(self, http_code, **kwargs):
        super(HTTPErrorSchema, self).__init__(**kwargs)
        self.fields['status_code'].default = http_code
