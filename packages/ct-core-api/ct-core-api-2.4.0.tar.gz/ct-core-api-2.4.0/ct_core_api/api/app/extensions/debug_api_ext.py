from ct_core_api.api.core.api import API


def _create_api(version):
    return API(version=version, title=u"Catalant Debugging API", description=u"Debugging Tools & Utilities")


debug_api_v2_0 = _create_api('2.0')


def init_app(app):
    app.register_extension(debug_api_v2_0, 'ct-debug-api-v2_0')
