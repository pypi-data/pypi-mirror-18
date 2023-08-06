"""
Extended API implementation with application-specific helpers
----------------------------------------------------------------
"""
from six import iteritems

from ct_core_api.api.core.namespace import APINamespace, APIAuthNamespace
from ct_core_api.api.lib.flask_restplus import Api


class API(Api):
    NAMESPACE = APINamespace

    def __init__(self, *args, **kwargs):
        super(API, self).__init__(*args, **kwargs)
        self.default_id = self._operation_id

    @staticmethod
    def _operation_id(resource, method):
        return '.'.join((resource, method))


class APIAuth(API):
    NAMESPACE = APIAuthNamespace

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

        super(APIAuth, self).add_namespace(ns)
