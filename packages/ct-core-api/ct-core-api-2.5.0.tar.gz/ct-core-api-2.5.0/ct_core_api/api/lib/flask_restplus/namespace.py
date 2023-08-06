from functools import wraps

import flask
import flask_marshmallow
from flask_restplus import Namespace as OriginalNamespace
from flask_restplus.utils import merge
from webargs.flaskparser import parser as webargs_parser
from werkzeug import exceptions as http_exceptions

from ._http import HTTPStatus
from .model import Model
from .parameters import Parameters
from .response import HTTPErrorSchema


class Namespace(OriginalNamespace):
    WEBARGS_PARSER = webargs_parser
    HTTP_ERROR_SCHEMA_CLS = HTTPErrorSchema
    ALLOWED_EMPTY_BODY_STATUSES = {HTTPStatus.NO_CONTENT, HTTPStatus.ACCEPTED}

    def _handle_api_doc(self, cls, doc):
        if doc is False:
            cls.__apidoc__ = False
            return
        cls.__apidoc__ = merge(getattr(cls, '__apidoc__', {}), doc)

    @staticmethod
    def resolve_object(object_arg_name, resolver):
        """
        A helper decorator to resolve object instance from arguments (e.g. identity).

        Example:
        >>> @namespace.route('/<int:user_id>')
        ... class MyResource(Resource):
        ...    @namespace.resolve_object(
        ...        object_arg_name='user',
        ...        resolver=lambda kwargs: User.query.get_or_404(kwargs.pop('user_id')))
        ...    def get(self, user):
        ...        # user is a User instance here
        """
        def decorator(func_or_class):
            if isinstance(func_or_class, type):
                # Handle Resource classes decoration
                func_or_class._apply_decorator_to_methods(decorator)
                return func_or_class

            @wraps(func_or_class)
            def wrapper(*args, **kwargs):
                kwargs[object_arg_name] = resolver(kwargs)
                return func_or_class(*args, **kwargs)
            return wrapper
        return decorator

    def model(self, name=None, model=None, mask=None, **kwargs):
        """
        Model registration decorator.
        """
        if isinstance(model, flask_marshmallow.Schema):
            if not name:
                name = model.__class__.__name__
            api_model = Model(name, model, mask=mask)
            api_model.__apidoc__ = kwargs
            return self.add_model(name, api_model)
        return super(Namespace, self).model(name, model, **kwargs)

    def parameters(self, parameters, locations=None):
        """
        Endpoint parameters registration decorator.
        """
        def decorator(func):
            if locations is None:
                _locations = ('json', )
                if isinstance(parameters, Parameters) and parameters.default_locations:
                    _locations = parameters.default_locations

            parameters.context['in'] = _locations

            return self.doc(params=parameters)(
                self.response(code=http_exceptions.UnprocessableEntity.code)(
                    self.WEBARGS_PARSER.use_args(parameters, locations=_locations)(func)))

        return decorator

    def response(self, model=None, code=200, description=None, **kwargs):
        """
        Endpoint response OpenAPI documentation decorator.

        It automatically documents HTTPError%(code)d responses with relevant
        schemas.

        Arguments:
            model (flask_marshmallow.Schema) - it can be a class or an instance
                of the class, which will be used for OpenAPI documentation
                purposes. It can be omitted if ``code`` argument is set to an
                error HTTP status code.
            code (int) - HTTP status code which is documented.
            description (str)

        Example:
        >>> @namespace.response(BaseTeamSchema(many=True))
        ... @namespace.response(code=403)
        ... def get_teams():
        ...     if not user.is_admin:
        ...         abort(403)
        ...     return Team.query.all()
        """

        if model is None and code not in self.ALLOWED_EMPTY_BODY_STATUSES:
            if code not in http_exceptions.default_exceptions:
                raise ValueError("`model` parameter is required for code {}".format(code))
            model = self.model(name="HTTPError{}".format(code), model=self.HTTP_ERROR_SCHEMA_CLS(http_code=code))

        if description is None:
            if code in http_exceptions.default_exceptions:
                description = http_exceptions.default_exceptions[code].description
            elif code in self.ALLOWED_EMPTY_BODY_STATUSES:
                description = u'Request fulfilled, nothing follows'

        def response_serializer_decorator(func):
            """
            This decorator handles responses to serialize the returned value
            with a given model.
            """
            def dump_wrapper(*args, **kwargs):
                response = func(*args, **kwargs)

                if response is None:
                    if code in self.ALLOWED_EMPTY_BODY_STATUSES:
                        return flask.Response(status=code, content_type='application/json')
                    raise ValueError('Response must not be empty with code 200')
                elif isinstance(response, flask.Response) or model is None:
                    return response
                elif isinstance(response, tuple):
                    response, _code = response
                else:
                    _code = code

                return model.dump(response).data, _code

            return dump_wrapper

        def decorator(func_or_class):
            if code in http_exceptions.default_exceptions:
                # If the code is handled by raising an exception, it will
                # produce a response later, so we don't need to apply a useless
                # wrapper.
                decorated_func_or_class = func_or_class
            elif isinstance(func_or_class, type):
                # Handle Resource classes decoration
                func_or_class._apply_decorator_to_methods(response_serializer_decorator)
                decorated_func_or_class = func_or_class
            else:
                decorated_func_or_class = wraps(func_or_class)(response_serializer_decorator(func_or_class))

            if code in self.ALLOWED_EMPTY_BODY_STATUSES:
                api_model = None
            else:
                if isinstance(model, Model):
                    api_model = model
                else:
                    api_model = self.model(model=model)
                if getattr(model, 'many', False):
                    api_model = [api_model]

            return self.doc(responses={code: (description, api_model)})(decorated_func_or_class)

        return decorator

    def route(self, *args, **kwargs):
        base_wrapper = super(Namespace, self).route(*args, **kwargs)

        def wrapper(cls):
            if 'OPTIONS' in cls.methods:
                cls.options = self.response(code=HTTPStatus.NO_CONTENT)(cls.options)
            return base_wrapper(cls)
        return wrapper
