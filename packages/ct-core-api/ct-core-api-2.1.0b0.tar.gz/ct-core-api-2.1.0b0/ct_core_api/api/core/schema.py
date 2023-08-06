from flask_marshmallow import Marshmallow

from ct_core_api.api.lib.flask_restplus import schema


class APISchema(schema.Schema):
    pass

########################################
# Marshmallow
########################################

ma = marshmallow = Marshmallow()

# FIXME: Update custom marshmallow fields
# FIXME: Update default marshmallow SchemaOpts
# FIXME: Include SchemaView integration?
# FIXME: Include method and function fields with schema return types?
# Attach our classes to the Flask-Marshmallow extension
# ma.SchemaOpts = SchemaOpts
# ma.Enum = ma_ext_fields.Enum = Enum
# ma.Html = ma_ext_fields.Html = Html
# ma.Nested = ma_ext_fields.Nested = Nested
# ma.Method = ma_ext_fields.Method = Method
# ma.Function = ma_ext_fields.Function = Function
# ma.ExternalId = ma_ext_fields.ExternalId = ExternalId
# ma.NullableString = ma_ext_fields.NullableString = NullableString
# ma.NullableInteger = ma_ext_fields.NullableInteger = NullableInteger
