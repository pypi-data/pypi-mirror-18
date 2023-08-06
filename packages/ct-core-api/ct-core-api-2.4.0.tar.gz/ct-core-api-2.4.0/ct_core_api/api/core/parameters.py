from marshmallow import validate
from six import itervalues

from ct_core_api.api.core.schema import ma
from ct_core_api.api.lib.flask_restplus.parameters import *  # noqa
from ct_core_api.api.lib.flask_restplus.parameters import Parameters


# FIXME: Figure out how to prevent Swagger UI from parsing the URL if webargs is doing the parsing
class URLParameters(Parameters):
    def __init__(self, **kwargs):
        super(URLParameters, self).__init__(**kwargs)
        for field in itervalues(self.fields):
            if field.dump_only:
                continue
            if not field.metadata.get('location'):
                field.metadata['location'] = 'view_args'


class PaginationParameters(Parameters):
    DEFAULT_LIMIT = 20
    DEFAULT_MAX_LIMIT = 100

    limit = ma.Integer(
        description="Limit the number of items (allowed range is 1-{}), default is {}.".format(
            DEFAULT_MAX_LIMIT, DEFAULT_LIMIT),
        missing=DEFAULT_LIMIT,
        validate=validate.Range(min=1, max=DEFAULT_MAX_LIMIT))

    offset = ma.Integer(
        description="The number of items to skip, default is 0.",
        missing=0,
        validate=validate.Range(min=0))
