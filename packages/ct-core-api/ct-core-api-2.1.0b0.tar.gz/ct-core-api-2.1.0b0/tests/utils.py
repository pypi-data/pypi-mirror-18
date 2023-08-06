"""
Testing utils
-------------
"""

import json
from contextlib import contextmanager
from datetime import datetime, timedelta

from flask import Response, url_for
from flask.testing import FlaskClient
from werkzeug.utils import cached_property


class JSONResponse(Response):
    """
    A Response class with extra useful helpers, i.e. ``.json`` property.
    """

    @cached_property
    def json(self):
        return json.loads(self.get_data(as_text=True))


# FIXME: Move to some service layer
def create_oauth2_bearer_token(user, auth_scopes):
    from ct_api_user_auth.app.modules.auth.models import OAuth2Token
    from ct_core_api.core.database import db

    oauth2_bearer_token = OAuth2Token(
        client_id=0,
        user=user,
        token_type='Bearer',
        access_token='test_access_token',
        _scopes=' '.join(auth_scopes),
        expires=datetime.utcnow() + timedelta(days=1))

    db.session.add(oauth2_bearer_token)
    db.session.commit()
    return oauth2_bearer_token


def remove_oauth2_bearer_token(oauth2_bearer_token):
    from ct_core_api.core.database import db
    db.session.delete(oauth2_bearer_token)
    db.session.commit()


class AppClient(FlaskClient):
    def url_for(self, endpoint, **values):
        with self.application.test_request_context('/'):
            return url_for(endpoint, **values)


class AuthAwareAppClient(AppClient):
    """
    A helper FlaskClient class with a ``login`` contextmanager.
    """

    def __init__(self, *args, **kwargs):
        super(AuthAwareAppClient, self).__init__(*args, **kwargs)
        self._user = None
        self._auth_scopes = None

    @contextmanager
    def login(self, user, auth_scopes=None):
        """
        Example:
            >>> with app_client.login(user, auth_scopes=['users:read']):
            ...     app_client.get('/api/v1/users/')
        """
        self._user = user
        self._auth_scopes = auth_scopes or []
        yield self
        self._user = None
        self._auth_scopes = None

    def open(self, *args, **kwargs):
        if self._user is not None:
            oauth2_bearer_token = create_oauth2_bearer_token(self._user, self._auth_scopes)

            extra_headers = (
                ('Authorization', '{token.token_type} {token.access_token}'.format(token=oauth2_bearer_token)),)
            if kwargs.get('headers'):
                kwargs['headers'] += extra_headers
            else:
                kwargs['headers'] = extra_headers

        response = super(AuthAwareAppClient, self).open(*args, **kwargs)

        if self._user is not None:
            remove_oauth2_bearer_token()

        return response


def generate_user_instance(
        user_id=None,
        username="username",
        password=None,
        email=None,
        first_name="First Name",
        middle_name="Middle Name",
        last_name="Last Name",
        created=None,
        updated=None,
        is_active=True,
        is_readonly=False,
        is_admin=False):
    """
    Returns:
        user_instance (User) - an not committed to DB instance of a User model.
    """
    from ct_api_user_auth.app.modules.user.models import User
    if password is None:
        password = "{}_password".format(username)
    user_instance = User(
        id=user_id,
        username=username,
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        password=password,
        email=email or "{}@email.com".format(username),
        created=created or datetime.now(),
        updated=updated or datetime.now(),
        is_active=is_active,
        is_readonly=is_readonly,
        is_admin=is_admin)
    user_instance.password_secret = password
    return user_instance
