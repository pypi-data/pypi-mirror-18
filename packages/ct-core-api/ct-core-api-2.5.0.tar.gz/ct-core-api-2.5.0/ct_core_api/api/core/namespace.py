"""
Extended Api Namespace implementation with an application-specific helpers
--------------------------------------------------------------------------
"""
from contextlib import contextmanager
from functools import wraps

import flask_marshmallow
import sqlalchemy
from werkzeug.exceptions import HTTPException

from ct_core_api.api.core import parser, response, schema
from ct_core_api.api.core.auth import user_permissions
from ct_core_api.api.core.response import APIErrorSchema
from ct_core_api.api.lib.flask_restplus import Namespace


class APINamespace(Namespace):
    WEBARGS_PARSER = parser.WebargsParser()
    HTTP_ERROR_SCHEMA_CLS = APIErrorSchema

    def model(self, name=None, model=None, **kwargs):
        """
        A decorator which registers a model (aka schema / definition).

        This extended implementation auto-generates a name for
        ``Flask-Marshmallow.Schema``-based instances by using a class name
        with stripped off `Schema` or `APISchema` prefixes.
        """
        if not name and isinstance(model, flask_marshmallow.Schema):
            name = model.__class__.__name__
            api_schema_cls_name = schema.APISchema.__name__
            schema_cls_name = flask_marshmallow.Schema.__name__
            if name.endswith(api_schema_cls_name):
                name = name[:-len(api_schema_cls_name)]
            elif name.endswith(schema_cls_name):
                name = name[:-len(schema_cls_name)]
        return super(APINamespace, self).model(name=name, model=model, **kwargs)

    @staticmethod
    def find_or_abort(abort_code, find_func, find_by_arg, abort_message=None, **abort_kwargs):
        obj = find_func(find_by_arg)
        if obj is None:
            response.abort(abort_code, message=abort_message, **abort_kwargs)
        return obj

    def resolve_object_by_find(
            self,
            object_arg_name,
            find_func,
            find_by_arg_name='id',
            abort_code=404,
            abort_message=None,
            **abort_kwargs):
        """Decorator that resolves an object instance by lookup.

        :param object_arg_name: argument name for the resolved object.
        :param find_func: a lookup function to resolve an object,
            takes the parsed value identified by `find_by_arg_name` as an only argument.
            Aborts with a 404 (default) response if the resolved object is None.
        :param find_by_arg_name: argument name holding the lookup value.
        :param abort_code: the response code used when no object is located.
        :param abort_message: optional abort message.

        Example:
        >>> @api.resolve_object_by_find('user', user_service.get_user_by_id)
        ... def get_user_by_id(user):
        ...     return user
        >>> get_user_by_id(user_id=3)
        <User(id=3, ...)>
        """
        # FIXME: Automatically document response using the `response` decorator
        return self.resolve_object(
            object_arg_name,
            resolver=lambda kwargs: self.find_or_abort(
                abort_code, find_func, kwargs.pop(find_by_arg_name), abort_message=abort_message, **abort_kwargs))

    @contextmanager
    def commit_or_abort(self, session, default_error_message="The operation failed to complete"):
        """
        Context manager to simplify a workflow in resources

        Args:
            session: db.session instance
            default_error_message: Custom error message

        Example:
        >>> api = APINamespace('/teams')
        ... with api.commit_or_abort(db.session):
        ...     team = Team(**args)
        ...     db.session.add(team)
        ...     return team
        """
        try:
            try:
                yield session
                session.commit()
            except ValueError as exception:
                response.abort(code=response.Conflict.code, message=str(exception))
            except sqlalchemy.exc.IntegrityError:
                response.abort(code=response.Conflict.code, message=default_error_message)
        except HTTPException:
            session.rollback()
            raise


class APIOAuthNamespace(APINamespace):
    OAUTH2_PROVIDER = None

    def login_required(self, oauth_scopes):
        """
        A decorator which restricts access for authorized user only.

        This decorator automatically applies the following features:

        * ``OAuth2.require_oauth`` decorator requires authentication;
        * All of the above requirements are put into OpenAPI Specification with
          relevant options and in a text description.

        Arguments:
            oauth_scopes (list) - a list of required OAuth2 Scopes (strings)

        Example:
        >>> api = APIOAuthNamespace('/users')
        ... class Users(APIResource):
        ...     @api.login_required(oauth_scopes=['users:read'])
        ...     def get(self):
        ...         return []
        """
        def decorator(func_or_class):
            if isinstance(func_or_class, type):
                # Handle Resource classes decoration
                func_or_class._apply_decorator_to_methods(decorator)
                return func_or_class
            else:
                func = func_or_class

            # Avoid circular dependency
            # This way we will avoid unnecessary checks if the decorator is
            # applied several times, e.g. when Resource class is decorated.
            func.__dict__['__latest_oauth_decorator_id__'] = id(decorator)

            # Automatically apply `permissions.ActiveUserRolePermission` guard if none is yet applied.
            if getattr(func, '_role_permission_applied', False):
                protected_func = func
            else:
                protected_func = self.permission_required(user_permissions.ActiveUserRolePermission())(func)

            # Ignore the current OAuth2 scopes if another @login_required
            # decorator was applied and just copy the already applied scopes.
            if (hasattr(protected_func, '__apidoc__') and
                    'security' in protected_func.__apidoc__ and
                    '__oauth__' in protected_func.__apidoc__['security']):
                _oauth_scopes = protected_func.__apidoc__['security']['__oauth__']['scopes']
            else:
                _oauth_scopes = oauth_scopes

            oauth_protection_decorator = self.OAUTH2_PROVIDER.require_oauth(*_oauth_scopes)
            self._register_access_restriction_decorator(protected_func, oauth_protection_decorator)
            oauth_protected_func = oauth_protection_decorator(protected_func)

            # This is a temporary configuration which is overridden in `API.add_namespace`.
            return self.doc(security={'__oauth__': {'type': 'oauth', 'scopes': _oauth_scopes}})(
                self.response(
                    code=response.Unauthorized.code,
                    description=(
                        u"Authentication is required"
                        if not _oauth_scopes else
                        u"Authentication with {} OAuth scope(s) is required".format(', '.join(_oauth_scopes))))(
                    oauth_protected_func))

        return decorator

    def permission_required(self, permission, kwargs_on_request=None):
        """
        A decorator which restricts access for users with a specific
        permissions user

        This decorator puts together permissions restriction code with OpenAPI
        Specification documentation.

        Arguments:
            permission (Permission) - it can be a class or an instance of
                :class:``Permission``, which will be applied to a decorated
                function, and docstrings of which will be used in OpenAPI
                Specification.
            kwargs_on_request (func) - a function which should accept only one
                ``dict`` argument (all kwargs passed to the function), and
                must return a ``dict`` of arguments which will be passed to
                the ``permission`` object.

        Example:
        >>> @namespace.permission_required(
        ...     OwnerRolePermission,
        ...     kwargs_on_request=lambda kwargs: {'obj': kwargs['team']})
        ... def get_team(team):
        ...     # This line will be reached only if OwnerRolePermission check is passed!
        ...     return team
        """
        def decorator(func):
            if getattr(permission, '_partial', False):
                # We don't apply partial permissions, we only use them for documentation purposes.
                protected_func = func
            else:
                if not kwargs_on_request:
                    _permission_decorator = permission
                else:
                    def _permission_decorator(func):
                        @wraps(func)
                        def wrapper(*args, **kwargs):
                            with permission(**kwargs_on_request(kwargs)):
                                return func(*args, **kwargs)
                        return wrapper

                protected_func = _permission_decorator(func)
                self._register_access_restriction_decorator(protected_func, _permission_decorator)

            permission_description = permission.__doc__.strip()
            return self.doc(description=u"**PERMISSIONS: {}**\n\n".format(permission_description))(
                self.response(
                    code=response.Forbidden.code,
                    description=permission_description)(
                    protected_func))

        return decorator

    @staticmethod
    def _register_access_restriction_decorator(func, decorator_to_register):
        """
        Helper function to register decorator to function to perform checks
        in options method
        """
        if not hasattr(func, '_access_restriction_decorators'):
            func._access_restriction_decorators = []
        func._access_restriction_decorators.append(decorator_to_register)
