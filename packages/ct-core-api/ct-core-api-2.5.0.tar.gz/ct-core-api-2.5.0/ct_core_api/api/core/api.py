"""
Extended API implementation with application-specific helpers
----------------------------------------------------------------
"""
from flask import render_template
from flask_restplus import representations
from six import iteritems

from ct_core_api.api.common import json_utils as ju
from ct_core_api.api.core import errors
from ct_core_api.api.core.namespace import APINamespace, APIOAuthNamespace
from ct_core_api.api.lib.flask_restplus import Api


# Monkey-patch Flask-RestPlus's JSON dumps function with our own
representations.dumps = ju.dumps


class API(Api):
    NAMESPACE = APINamespace

    def __init__(self, *args, **kwargs):
        super(API, self).__init__(*args, **kwargs)
        # Modify how an operation identifier gets generated in Swagger
        self.default_id = self._operation_id
        # Register the default error handlers
        self.error_handlers = {}
        errors.register_error_handlers(self)

    @staticmethod
    def _operation_id(resource, method):
        return '.'.join((resource, method))

    def _register_apidoc(self, app):
        # Prevent Flask-RestPlus from registering it's `apidoc` blueprint so that we can use our own.
        pass

    def render_doc(self):
        return render_template('swagger-ui/swagger-ui.html', title=self.title, specs_url=self.specs_url)


class APIOAuth(API):
    NAMESPACE = APIOAuthNamespace

    def add_oauth_scope(self, scope_name, scope_description):
        for authorization_settings in self.authorizations.values():
            if authorization_settings['type'].startswith('oauth'):
                assert scope_name not in authorization_settings['scopes'], \
                    "OAuth scope {} already exists".format(scope_name)
                authorization_settings['scopes'][scope_name] = scope_description

    def add_namespace(self, ns):
        # Rewrite security rules for OAuth scopes since Namespaces don't have
        # enough information about authorization methods.
        for resource, _, _ in ns.resources:
            for method in resource.methods:
                method_func = getattr(resource, method.lower())

                api_doc = getattr(method_func, '__apidoc__', {})
                if 'security' in api_doc and '__oauth__' in api_doc['security']:
                    oauth_scopes = api_doc['security']['__oauth__']['scopes']
                    method_func.__apidoc__['security'] = {
                        auth_name: oauth_scopes
                        for auth_name, auth_settings in iteritems(self.authorizations)
                        if auth_settings['type'].startswith('oauth')}

        super(APIOAuth, self).add_namespace(ns)
