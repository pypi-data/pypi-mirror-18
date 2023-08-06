from ct_core_api.api.core import schema


########################################
# Marshmallow Extension
########################################

def init_app(app):
    schema.ma.init_app(app)
