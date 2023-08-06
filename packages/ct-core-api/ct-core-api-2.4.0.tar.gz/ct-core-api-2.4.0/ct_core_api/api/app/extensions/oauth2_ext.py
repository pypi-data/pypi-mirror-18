"""
OAuth2 provider setup.

It is based on the code from the example:
https://github.com/lepture/example-oauth2-server

More details are available here:
* http://flask-oauthlib.readthedocs.org/en/latest/oauth2.html
* http://lepture.com/en/2013/create-oauth-server
"""

import logging
from datetime import datetime, timedelta

from flask_login import current_user
from flask_oauthlib import provider

from ct_core_api.api.core import response

_logger = logging.getLogger(__name__)


def init_app(app):
    from ct_core_api.api.app.extensions import login_manager_ext
    from ct_core_api.api.core.namespace import APIOAuthNamespace

    APIOAuthNamespace.OAUTH2_PROVIDER = oauth2

    login_manager_ext.login_manager.request_loader(_load_user_from_request)
    oauth2.init_app(app)


class InternalAuthManagementService(object):
    # FIXME: Figure out how the operations are named by our internal API clients
    def __init__(self, user_internal_api_client, auth_internal_api_client):
        self._user_internal_api_client = user_internal_api_client
        self._auth_internal_api_client = auth_internal_api_client

    # User
    def get_user_by_username_password(self, username, password):
        return self._user_internal_api_client.get_user_by_username_password(username, password)

    # OAuth2 Client
    def get_client_by_client_id(self, client_id):
        return self._auth_internal_api_client.get_oauth2_client_by_client_id(client_id)

    # OAuth2 Token
    def get_token_by_access_or_refresh_token(self, access_token=None, refresh_token=None):
        return self._auth_internal_api_client.get_oauth2_token_by_refresh_or_access_token(access_token, refresh_token)

    def create_token(self, access_token, token_type, scopes, expires, client_id, user_id, refresh_token=None):
        return self._auth_internal_api_client.create_token(
            access_token, token_type, scopes, expires, client_id, user_id, refresh_token)

    # OAuth2 Grant
    def get_grant_by_client_id_and_code(self, client_id, code):
        return self._auth_internal_api_client.get_oauth2_grant_by_client_id_and_code(client_id, code)

    def create_grant(self, client_id, user, code, scopes, expires, redirect_uri):
        return self._auth_internal_api_client.create_grant(client_id, user, code, scopes, expires, redirect_uri)


class OAuth2RequestValidator(provider.OAuth2RequestValidator):
    def __init__(self, internal_auth_mgmt_service):
        self._internal_auth_mgmt_service = internal_auth_mgmt_service
        super(OAuth2RequestValidator, self).__init__(
            usergetter=self._user_getter,
            clientgetter=self._client_getter,
            tokengetter=self._token_getter,
            tokensetter=self._token_setter,
            grantgetter=self._grant_getter,
            grantsetter=self._grant_setter)

    def _user_getter(self, username, password, client, request):
        return self._internal_auth_mgmt_service.get_user_by_username_password(username, password)

    def _client_getter(self, client_id):
        return self._internal_auth_mgmt_service.get_client_by_client_id(client_id)

    def _token_getter(self, access_token=None, refresh_token=None):
        return self._internal_auth_mgmt_service.get_token_by_access_or_refresh_token(access_token, refresh_token)

    def _token_setter(self, token, request, *args, **kwargs):
        access_token = token['access_token'],
        token_type = token['token_type'],
        scopes = token['scope'].split(),
        expires = datetime.utcnow() + timedelta(seconds=token['expires_in'])
        refresh_token = token.get('refresh_token'),

        client_id = request.client.client_id
        user_id = request.user.id

        return self._internal_auth_mgmt_service.create_token(
            access_token, token_type, scopes, expires, client_id, user_id, refresh_token)

    def _grant_getter(self, client_id, code):
        return self._internal_auth_mgmt_service.get_grant_by_client_id_and_code(client_id, code)

    def _grant_setter(self, client_id, code, request, *args, **kwargs):
        # FIXME: Use configurable grant expiry time
        expires = datetime.utcnow() + timedelta(seconds=100)
        redirect_uri = request.redirect_uri
        scopes = request.scopes
        return self._internal_auth_mgmt_service.create_grant(
            client_id, current_user, code, scopes, expires, redirect_uri)

    def client_authentication_required(self, request, *args, **kwargs):
        # XXX: patched version
        # TODO: implement it better in oauthlib, but for now we excluded
        # password flow from `client_secret` requirement.
        grant_types = ('authorization_code', 'refresh_token')
        return request.grant_type in grant_types


def invalid_oauth_response(req):
    """Default handler of invalid responses from `OAuth2Provider`"""
    response.abort(code=response.Unauthorized.code)


class OAuth2Provider(provider.OAuth2Provider):
    """A helper class which connects OAuth2RequestValidator with OAuth2Provider."""

    def __init__(self, *args, **kwargs):
        super(OAuth2Provider, self).__init__(*args, **kwargs)
        self.invalid_response(invalid_oauth_response)

    def init_app(self, app):
        super(OAuth2Provider, self).init_app(app)
        # FIXME: Provide the internal user and auth clients
        internal_auth_mgmt_service = InternalAuthManagementService(None, None)
        self._validator = OAuth2RequestValidator(internal_auth_mgmt_service)


oauth2 = OAuth2Provider()


def _load_user_from_request(request):
    """Load user from OAuth2 Authentication header."""
    user = None
    if hasattr(request, 'oauth'):
        user = request.oauth.user
    else:
        is_valid, oauth = oauth2.verify_request(scopes=[])
        if is_valid:
            user = oauth.user
    return user
