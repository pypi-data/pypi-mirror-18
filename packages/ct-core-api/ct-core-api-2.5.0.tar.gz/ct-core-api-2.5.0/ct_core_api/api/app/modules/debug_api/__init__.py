from ct_core_api.api.app.extensions import debug_api_ext
from ct_core_api.api.common import api_helpers as ah


def init_app(app):
    ah.register_api_resources(
        app, debug_api_ext.debug_api_v2_0, __path__, __name__, blueprint_prefix='debug-api', url_prefix='/_debug/api')
