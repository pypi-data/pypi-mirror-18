from webargs.flaskparser import FlaskParser

from ct_core_api.api.core import response


class WebargsParser(FlaskParser):
    """
    This custom Webargs Parser aims to overload :meth:``handle_error`` in order
    to call our custom :func:``abort`` function.

    See the following issue and the related PR for more details:
    https://github.com/sloria/webargs/issues/122
    """

    def handle_error(self, error):
        """
        Handles errors during parsing. Aborts the current HTTP request and
        responds with a 422 error.
        """
        status_code = getattr(error, 'status_code', self.DEFAULT_VALIDATION_STATUS)
        response.abort(status_code, messages=error.messages)
