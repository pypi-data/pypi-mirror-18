def init_app(app):
    from ct_core_api.api.app.modules.index import index_views
    app.register_blueprint(index_views.bp)
