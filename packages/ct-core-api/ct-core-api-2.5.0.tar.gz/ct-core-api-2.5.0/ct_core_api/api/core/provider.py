

########################################
# User Provider
########################################

class UserProvider(object):
    def __init__(self):
        self._user_by_id_getter = None
        self._user_by_email_getter = None
        self._user_for_auth_token_getter = None
        self._user_for_secret_id_getter = None
        self._anonymous_user_getter = None

    # ==================================
    # Decorators for user provider
    # ==================================
    def user_by_id_getter(self, f):
        self._user_by_id_getter = f

    def user_by_email_getter(self, f):
        self._user_by_email_getter = f

    def user_for_auth_token_getter(self, f):
        self._user_for_auth_token_getter = f

    def user_for_secret_id_getter(self, f):
        self._user_for_secret_id_getter = f

    def anonymous_user_getter(self, f):
        self._anonymous_user_getter = f

    # ==================================
    # Functions for user consumer
    # ==================================
    def get_user_by_id(self, id):
        if self._user_by_id_getter:
            return self._user_by_id_getter(id)
        raise NotImplementedError(
            'Decorate the function that will "get a user by id" with `user_by_id_getter`')

    def get_user_by_email(self, email):
        if self._user_by_email_getter:
            return self._user_by_email_getter(email)
        raise NotImplementedError(
            'Decorate the function that will "get a user by email" with `user_by_email_getter`')

    def get_user_for_auth_token(self, auth_token):
        if self._user_for_auth_token_getter:
            return self._user_for_auth_token_getter(auth_token)
        raise NotImplementedError(
            'Decorate the function that will "get a user for an auth token" with `user_for_auth_token_getter`')

    def get_user_for_secret_id(self, secret_id):
        if self._user_for_secret_id_getter:
            return self._user_for_secret_id_getter(secret_id)
        raise NotImplementedError(
            'Decorate the function that will "get a user by secret id" with `user_by_secret_id_getter`')

    def get_anonymous_user(self):
        if self._anonymous_user_getter:
            return self._anonymous_user_getter()
        raise NotImplementedError(
            'Decorate the function that will "get an anonymous user" with `anonymous_user_getter`')


core_user_provider = UserProvider()


########################################
# Application Provider
########################################

class ApplicationProvider(object):
    def __init__(self):
        self._application_for_host_getter = None
        self._application_for_client_app_id_getter = None

    # ==================================
    # Decorators for application provider
    # ==================================
    def application_for_host_getter(self, f):
        self._application_for_host_getter = f

    def application_for_client_app_id_getter(self, f):
        self._application_for_client_app_id_getter = f

    # ==================================
    # Functions for application consumer
    # ==================================
    def get_application_for_host(self, host):
        if self._application_for_host_getter:
            return self._application_for_host_getter(host)
        raise NotImplementedError(
            'Decorate the function that will "get an application for a host" with `application_for_host_getter`')

    def get_application_for_client_app_id(self, client_app_id):
        if self._application_for_client_app_id_getter:
            return self._application_for_client_app_id_getter(client_app_id)
        raise NotImplementedError(
            'Decorate the function that will "get an application for a client app id" '
            'with `application_for_client_app_id_getter`')

core_application_provider = ApplicationProvider()


########################################
# Auth Token Provider
########################################

class AuthTokenProvider(object):
    def __init__(self):
        self._auth_token_generator = None

    # ==================================
    # Decorators for auth token provider
    # ==================================
    def auth_token_generator(self, f):
        self._auth_token_generator = f

    # ==================================
    # Functions for auth token consumer
    # ==================================
    def generate_auth_token_for_user(self, user):
        if self._auth_token_generator:
            return self._auth_token_generator(user)
        raise NotImplementedError(
            'Decorate the function that will "generate an auth token for a user" '
            'with `auth_token_generator`')


########################################
# Auth Provider
########################################

class AuthProvider(object):
    def __init__(self, user_provider, application_provider):
        self._user_provider = user_provider
        self._application_provider = application_provider

        self._user_has_application_access_verifier = None
        self._app_token_validator = None

    # ==================================
    # Decorators for auth provider
    # ==================================
    def user_has_application_access_verifier(self, f):
        self._user_has_application_access_verifier = f

    def app_token_validator(self, f):
        self._app_token_validator = f

    # ==================================
    # Functions for auth consumer
    # ==================================
    def get_application_for_host(self, host):
        return self._application_provider.get_application_for_host(host)

    def get_anonymous_user(self):
        return self._user_provider.get_anonymous_user()

    def get_user_for_auth_token(self, auth_token):
        return self._user_provider.get_user_for_auth_token(auth_token)

    def user_has_application_access(self, user, application):
        if self._user_has_application_access_verifier:
            return self._user_has_application_access_verifier(user, application)
        raise NotImplementedError(
            'Decorate the function that will "verify if a user has application access" '
            'with `user_has_application_access_verifier`')

    def validate_app_token(self, application, token):
        if self._app_token_validator:
            return self._app_token_validator(application, token)
        raise NotImplementedError(
            'Decorate the function that will "validate an app token" '
            'with `app_token_validator`')


core_auth_provider = AuthProvider(core_user_provider, core_application_provider)
