from ct_core_api.api.app.extensions import login_manager_ext, oauth2_ext


def load_user_from_request(request):
    """Load user from OAuth2 Authentication header."""
    user = None
    if hasattr(request, 'oauth'):
        user = request.oauth.user
    else:
        is_valid, oauth = oauth2_ext.oauth2.verify_request(scopes=[])
        if is_valid:
            user = oauth.user
    return user


def init_app(app):
    login_manager_ext.login_manager.request_loader(load_user_from_request)
