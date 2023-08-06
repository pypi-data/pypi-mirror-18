from ct_core_api.api.core.api import API

debug_api_v1 = API(version='1.0', title=u"Catalant Debugging API", description=u"Debugging Tools & Utilities")


def init_app(app, **kwargs):
    # FIXME: Determine if we need to host a custom Swagger-UI
    # if app.debug:
    #     @app.route('/swaggerui/<path:path>')
    #     def send_swaggerui_assets(path):
    #         from flask import send_from_directory
    #         return send_from_directory('../static/', path)

    app.register_extension(debug_api_v1, 'ct-debug-api-v1')
