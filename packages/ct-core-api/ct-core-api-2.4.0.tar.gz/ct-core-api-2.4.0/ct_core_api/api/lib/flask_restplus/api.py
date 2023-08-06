from flask import jsonify
from flask_restplus import Api as OriginalApi
from werkzeug import exceptions as http_exceptions
from werkzeug.utils import cached_property

from .namespace import Namespace
from .swagger import Swagger


class Api(OriginalApi):
    SWAGGER = Swagger
    NAMESPACE = Namespace

    @cached_property
    def __schema__(self):
        # The only purpose of this method is to pass custom Swagger class
        return self.SWAGGER(self).as_dict()

    def init_app(self, app, **kwargs):
        super(Api, self).init_app(app, **kwargs)
        app.errorhandler(http_exceptions.UnprocessableEntity.code)(handle_validation_error)

    def namespace(self, *args, **kwargs):
        # The only purpose of this method is to pass a custom Namespace class
        _namespace = self.NAMESPACE(*args, **kwargs)
        self.add_namespace(_namespace)
        return _namespace


# Return validation errors as JSON
def handle_validation_error(err):
    exc = err.data['exc']
    return jsonify({
        'status': http_exceptions.UnprocessableEntity.code,
        'message': exc.messages
    }), http_exceptions.UnprocessableEntity.code
