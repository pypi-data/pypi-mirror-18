import logging

from flask import current_app
from marshmallow import validate

from ct_core_api.api.core.namespace import APINamespace
from ct_core_api.api.core.parameters import PostFormParameters
from ct_core_api.api.core.resource import APIResource
from ct_core_api.api.core.response import HTTPStatus
from ct_core_api.api.core.schema import ma

api = APINamespace('log', description="Logging Utilities")


@api.route('/')
class LoggingResource(APIResource):
    class PostParameters(PostFormParameters):
        level = ma.Str(
            required=True,
            location='form',
            validate=validate.OneOf(choices=[
                logging.getLevelName(logging.DEBUG),
                logging.getLevelName(logging.INFO),
                logging.getLevelName(logging.WARNING),
                logging.getLevelName(logging.ERROR),
                logging.getLevelName(logging.CRITICAL)]))
        message = ma.Str(required=True, location='form')

    @api.parameters(PostParameters())
    @api.response(code=HTTPStatus.NO_CONTENT)
    def post(self, args):
        """Log a message at the specified log level."""
        current_app.logger.log(logging.getLevelName(args['level']), args['message'])
