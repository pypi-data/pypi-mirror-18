def init_app(app):
    @app.route('/health/ping')
    def ping():
        """Simplistic health check route that many of our internal checks expect to exist."""
        return u'OK', 200
