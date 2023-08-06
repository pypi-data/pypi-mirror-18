from werkzeug import exceptions as http_exceptions
from werkzeug.http import HTTP_STATUS_CODES

from ct_core_api.api.core import response


def register_error_handlers(api):
    # Note: Error handler functions must include a docstring!
    # It provides the error's description in the "responses" section of the Swagger specification.
    from flask_principal import PermissionDenied
    from sqlalchemy.orm.exc import NoResultFound
    from validation21 import ValidationException

    @api.errorhandler
    def handle_unregistered_error(e):
        # Call the first error handler that matches based on inheritance
        for exception_cls in api.error_handlers:
            if isinstance(e, exception_cls):
                return api.error_handlers[exception_cls](e)
        return handle_500_error(e)

    @api.errorhandler(http_exceptions.HTTPException)
    def handle_http_exception_error(e):
        """An HTTP error occurred."""
        return prepare_error_response(e, e.code, headers=e.get_response().headers)

    @api.errorhandler(http_exceptions.UnprocessableEntity)
    def handle_unprocessable_entity_error(e):
        """The request is well formed, but the instructions are otherwise incorrect (e.g. validation failed)."""
        exc = e.data['exc']
        prepare_error_response(e, e.code, message=exc.messages)

    api.errorhandler(PermissionDenied)(handle_403_error)
    api.errorhandler(NoResultFound)(handle_404_error)
    api.errorhandler(ValidationException)(handle_422_error)


def resolve_error_message(e, fallback_message=None):
    data = getattr(e, 'data', {})
    return str(data.get('message', fallback_message or e))


def prepare_error_response(e, status_code, message=None, error_code=None, params=None, headers=None):
    message = message or resolve_error_message(e, HTTP_STATUS_CODES.get(status_code))
    # Flask-RestPlus's downstream error handling will ignore the data we return if this isn't removed
    if hasattr(e, 'data'):
        delattr(e, 'data')
    return response.generate_api_error_response(message, status_code, error_code, params, headers)


########################################
# Error Handlers
########################################

def handle_403_error(e):
    """The user doesn't have the permission for the requested resource but was authenticated."""
    # TODO: Enhance error message with information from `PermissionDenied`
    return prepare_error_response(e, 403)


def handle_404_error(e):
    """A resource does not exist and never existed."""
    return prepare_error_response(e, 404)


def handle_422_error(e):
    """The request is well formed, but the instructions are otherwise incorrect."""
    # TODO: Create `params` data from `ValidationException` and `ValidationError`
    # if e.error_dict:
    #     errors = {}
    #     for k, v in e.error_dict:
    #         errors[v.field] = e.message
    # else:
    #     errors = {e.field: e.message}
    return prepare_error_response(e, 422)


def handle_500_error(e):
    return prepare_error_response(e, 500)
