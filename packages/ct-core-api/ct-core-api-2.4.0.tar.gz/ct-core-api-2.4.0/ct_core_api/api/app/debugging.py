from ct_core_api.common import db_utils as dbu


def init_app(app):
    @app.before_first_request
    def configure_remote_debugging():
        if app.config.get('REMOTE_DEBUG', False):
            import pydevd
            ip = app.config.get('REMOTE_DEBUG_IP', '192.168.7.1')
            port = app.config.get('REMOTE_DEBUG_PORT', 34153)
            app.logger.info("Starting the remote debugger server at {0}:{1}".format(ip, port))
            pydevd.settrace(ip, port=port, stdoutToServer=True, stderrToServer=True, suspend=False)
            app.logger.info('Remote debugging...')

    @app.after_request
    def log_debug_sql_queries(response):
        if app.debug and app.config.get('API_LOG_DEBUG_SQL_QUERIES'):
            app.logger.debug(dbu.get_debug_queries_summary())
        return response

    @app.after_request
    def log_chrome_console_messages(response):
        if app.config.get('API_LOG_EXCEPTIONS_TO_BROWSER_CONSOLE', False):
            import chromelogger
            header = chromelogger.get_header()
            if header is not None:
                response.headers.add(header[0], header[1])
        return response
