from marshmallow import validate
from werkzeug import exceptions

from ct_core_api.api.core import response
from ct_core_api.api.core.namespace import APINamespace
from ct_core_api.api.core.parameters import PostFormParameters
from ct_core_api.api.core.resource import APIResource
from ct_core_api.api.core.response import HTTPStatus
from ct_core_api.api.core.schema import ma

api = APINamespace('error', description="Error/Exception Simulation Tools")


@api.route('/raise-status-code')
class ErrorStatusCodeResource(APIResource):
    class PostParameters(PostFormParameters):
        status_code = ma.Integer(
            required=True,
            location='form',
            validate=validate.OneOf(choices=exceptions.default_exceptions.keys()))

    @api.parameters(PostParameters())
    @api.response(code=HTTPStatus.NO_CONTENT)
    def post(self, args):
        """Raise an HTTP error for this status code."""
        response.abort(code=args['status_code'], message="HTTP error for status code: {}".format(args['status_code']))


@api.route('/raise-exception')
class ErrorExceptionResource(APIResource):
    @api.response(code=HTTPStatus.NO_CONTENT)
    def post(self, args):
        """Raise an Exception."""
        raise Exception('error')
