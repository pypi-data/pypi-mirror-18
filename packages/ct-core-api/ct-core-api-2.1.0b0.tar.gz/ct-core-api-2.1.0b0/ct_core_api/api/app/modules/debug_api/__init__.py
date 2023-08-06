from flask import Blueprint

from ct_core_api.api.app.extensions import debug_api_ext


def init_app(app):
    from ct_core_api.api.app.modules.debug_api import (
        cache_resources,
        config_resources,
        error_resources,
        log_resources)
    debug_api_ext.debug_api_v1.add_namespace(cache_resources.api)
    debug_api_ext.debug_api_v1.add_namespace(config_resources.api)
    debug_api_ext.debug_api_v1.add_namespace(error_resources.api)
    debug_api_ext.debug_api_v1.add_namespace(log_resources.api)

    debug_api_v1_blueprint = Blueprint('debug-api-v1', __name__, url_prefix='/_debug/api/v1')
    debug_api_ext.debug_api_v1.init_app(debug_api_v1_blueprint)
    app.register_blueprint(debug_api_v1_blueprint)
