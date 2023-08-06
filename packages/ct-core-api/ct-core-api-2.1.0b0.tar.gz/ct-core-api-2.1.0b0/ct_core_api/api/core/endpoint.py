import inspect
import functools
from datetime import datetime, timedelta

from flask import current_app, request

from ct_core_api.api.common import log_utils as lu
from ct_core_api.api.core import cache
from ct_core_api.api.core.swagger import doc_utils as du, handle_api_doc
from ct_core_api.common import datetime_utils as dtu


########################################
# Endpoint (Operation) Decorators
########################################

def doc(
        schema=None,
        schema_view=None,
        description=None,
        parser=None,
        params=None,
        search_parsers=None,
        search_params_doc=None,
        permissions=None,
        show=True,
        **kwargs):
    """Apply Swagger documentation to a Resource endpoint.
    The decorated function will be inspected and common input parameters will be included in the docs.
    """
    def wrapper(fn):
        fn_name = fn.__name__
        fn_args = filter(lambda x: x != 'self', inspect.getargspec(fn).args)  # Exclude the 'self' argument
        doc = du.doc_endpoint(
            fn_name,
            fn_args,
            schema=schema,
            schema_view=schema_view,
            description=description,
            search_parsers=search_parsers,
            search_params_doc=search_params_doc,
            params=params,
            parser=parser,
            permissions=permissions,
            **kwargs)
        handle_api_doc(fn, doc if show else False)
        return fn
    return wrapper


def deprecated(deprecated_on_date, deprecated_removal_date, reason=None):
    """Decorator marking an API endpoint as deprecated.
    If the current time is within the configured window (defaults to 1 week),
    a warning message will be logged to both the client's browser (when debug is enabled) and to the server.
    See configuration setting: `API_DEPRECATED_ENDPOINT_WARNING_WINDOW`

    Additionally, this endpoint operation will be annotated with it's deprecation details so that they can be
    documented in the API's Swagger specification.

    :param deprecated_on_date: When this endpoint was first marked for deprecation.
        Can be a date string with format: 'mm/dd/yyyy'
    :param deprecated_removal_date: The date on which this endpoint is scheduled to be removed.
        Can be a date string with format: 'mm/dd/yyyy'
    :param reason: Why this endpoint operation is being deprecated
        (ie. performance, changed inputs, changed response).
    """
    def decorator(func):
        # Convert formatted date strings in Eastern time to UTC datetimes, if needed
        dep_on = deprecated_on_date
        dep_removal = deprecated_removal_date

        if not isinstance(dep_on, datetime):
            dep_on = dtu.local_d_str_to_utc_datetime(dep_on, dtu.TimeZone.EASTERN)

        if not isinstance(dep_removal, datetime):
            dep_removal = dtu.local_d_str_to_utc_datetime(dep_removal, dtu.TimeZone.EASTERN)

        # Annotate this function with the deprecation details for Swagger documentation
        deprecation_doc = dict(
            deprecated=True,
            deprecated_on_date=dep_on,
            deprecated_removal_date=dep_removal)

        if reason:
            deprecation_doc['deprecated_reason'] = reason

        handle_api_doc(func, deprecation_doc)

        # Log warning messages if we've entered the deprecation warning window
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if current_app.config.get('API_LOG_VERBOSE_DEV_MESSAGES', False):
                client_warning_msg = "Deprecated endpoint: [{}] {}".format(request.method, request.path)
                lu.log_api_warning_message_to_browser_console(client_warning_msg)

            warning_window = current_app.config.get('API_DEPRECATED_ENDPOINT_WARNING_WINDOW', timedelta(weeks=1))

            if not dep_removal or datetime.utcnow() >= (dep_removal - warning_window):
                server_warning_msgs = [
                    "API client '{}' using deprecated endpoint!".format(
                        request.headers.get('X-App-Host', '<unknown>')),
                    "Deprecation schedule: {} - {}".format(
                        dtu.format_datetime_et(dep_on, "%m/%d/%Y"), dtu.format_datetime_et(dep_removal, "%m/%d/%Y"))]

                if reason:
                    server_warning_msgs.append("Reason: {}".format(reason))

                current_app.logger.warning('\n'.join(server_warning_msgs))

            return func(*args, **kwargs)

        return wrapper

    return decorator


def cache_data(region, key=None, ignore_user_context=False, ignore_application_context=False):
    """Decorator that will cache an API endpoint's response data.

    Note: This caches the data portion of the payload which excludes the headers, etc.

    Additionally, this endpoint operation will be annotated with the cache region's name and it's expiration time.

    :param region: Name of the cache region. See `DOGPILE_CACHE_REGIONS` in the application's configuration.
    :param key: The cache key for this region. Will be auto-generated from the request if not specified.
    :param ignore_user_context:
    Whether user context information should contribute to the generation of the cache key.
    :param ignore_application_context:
    Whether application context information should contribute to the generation of the cache key.
    """
    def decorator(func):
        cache_doc = dict(cache_region=region)
        handle_api_doc(func, cache_doc)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return cache.cache_response_data_fn(
                func,
                region,
                key,
                *args,
                ignore_user_context=ignore_user_context,
                ignore_application_context=ignore_application_context,
                **kwargs)
        return wrapper
    return decorator
