from flask_marshmallow import Marshmallow
from marshmallow import SchemaOpts, fields

from ct_core_api.api.common import json_utils as ju
from ct_core_api.api.lib.flask_restplus import schema


########################################
# API Schema & SchemaOpts
########################################

class APISchemaOpts(SchemaOpts):
    def __init__(self, meta):
        SchemaOpts.__init__(self, meta)
        # Raise errors if invalid data are passed in instead of failing silently and storing the errors
        self.strict = True
        # Use ISO8601-formatted datetimes
        self.dateformat = 'iso'
        # Our json module supports decimals, naive datetimes, and terse formatting
        self.json_module = ju


class APISchema(schema.Schema):
    OPTIONS_CLASS = APISchemaOpts


########################################
# Marshmallow Fields
########################################

fields.DateTime.DATEFORMAT_SERIALIZATION_FUNCS['iso'] = ju.isoformat
fields.DateTime.DATEFORMAT_SERIALIZATION_FUNCS['iso8601'] = ju.isoformat

fields.DateTime.DATEFORMAT_DESERIALIZATION_FUNCS['iso'] = ju.from_iso
fields.DateTime.DATEFORMAT_DESERIALIZATION_FUNCS['iso8601'] = ju.from_iso


########################################
# Marshmallow
########################################

ma = marshmallow = Marshmallow()

# Attach our classes to the Flask-Marshmallow extension
ma.SchemaOpts = SchemaOpts
# ma.Enum = ma_ext_fields.Enum = Enum
# ma.Html = ma_ext_fields.Html = Html
# ma.Nested = ma_ext_fields.Nested = Nested
# ma.Method = ma_ext_fields.Method = Method
# ma.Function = ma_ext_fields.Function = Function
# ma.ExternalId = ma_ext_fields.ExternalId = ExternalId
