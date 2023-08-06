from werkzeug.exceptions import NotFound
from werkzeug.wsgi import DispatcherMiddleware


def _not_found_response(environ, start_response):
    start_response(bytes(NotFound.code), [(b'Content-Type', b'text/plain')])
    return [NotFound.description.encode()]


class PrefixDispatcherMiddleware(DispatcherMiddleware):
    """Middleware that prefixes all relative application URLs with the provided value (include leading slashes).
    This operates by sub-mounting the application within the WSGI container using the `DispatcherMiddleware`.

    :See: http://stackoverflow.com/questions/18967441/add-a-prefix-to-all-flask-routes
    """
    def __init__(self, wsgi_app, prefix=''):
        super(PrefixDispatcherMiddleware, self).__init__(_not_found_response, {prefix: wsgi_app})


class PrefixMiddleware(object):
    """Middleware that prefixes all relative application URLs with the provided value (include leading slashes).
    This operates by modifying the WSGI `PATH_INFO` and `SCRIPT_NAME` environment variables.

    :See: https://gist.github.com/Larivact/1ee3bad0e53b2e2c4e40
    """

    def __init__(self, wsgi_app, prefix=''):
        self.wsgi_app = wsgi_app
        self.prefix = prefix

    def __call__(self, environ, start_response):
        if environ['PATH_INFO'].startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
            return self.wsgi_app(environ, start_response)
        else:
            return _not_found_response(environ, start_response)
