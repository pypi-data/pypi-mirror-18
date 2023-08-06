try:
    from http import HTTPStatus
except ImportError:
    class HTTPStatus(object):
        ACCEPTED = 202
        NO_CONTENT = 204
