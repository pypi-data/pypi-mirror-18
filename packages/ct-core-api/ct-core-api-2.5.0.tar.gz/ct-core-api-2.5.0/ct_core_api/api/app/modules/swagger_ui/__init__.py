def init_app(app):
    from ct_core_api.api.app.modules.swagger_ui import swagger_ui_views
    app.register_blueprint(swagger_ui_views.bp)
