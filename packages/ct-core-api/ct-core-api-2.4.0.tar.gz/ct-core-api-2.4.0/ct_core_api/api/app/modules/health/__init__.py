def init_app(app):
    from ct_core_api.api.app.modules.health import health_views
    app.register_blueprint(health_views.bp, url_prefix='/health')
