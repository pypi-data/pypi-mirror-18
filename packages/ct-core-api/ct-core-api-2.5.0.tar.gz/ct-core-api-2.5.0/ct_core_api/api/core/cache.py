import hashlib
from urlparse import urlparse, urlunparse

from dogpile.cache.api import NO_VALUE
from flask import current_app, g, request
from flask_dogpile_cache import DogpileCache

dogpile_cache = DogpileCache()


########################################
# Response Data Caching
########################################

def _can_use_response_data_cache():
    # TODO: Respect cache headers (ie. Cache-Control: no-cache)
    return True


def _create_response_data_cache_key(req, **context):
    key = hashlib.sha256()
    key_parts = []

    # Strip the protocol and fragment, leaving a relative URL with query params intact
    parsed_url = urlparse(req.url)
    unparsed_url = urlunparse((None, None, parsed_url.path, parsed_url.params, parsed_url.query, None))

    key_parts.append(req.method.upper())
    key_parts.append(unparsed_url)

    for name, value in sorted(req.form.iteritems()):
        key_parts.append(name)
        key_parts.append(value)

    for name, value in sorted(context.iteritems()):
        key_parts.append(name)
        key_parts.append(unicode(value))

    for key_part in key_parts:
        key.update(key_part)

    # current_app.logger.debug("response data cache key parts: {}".format(', '.join(key_parts)))

    return key.hexdigest()


def _generate_response_data_cache_key(include_user_context=True, include_application_context=True):
    """Generate the final cache key for use in caching response data.
    The cache key will have a unique signature that varies with:
    - cache key version
    - request information (URL, request method, form values)
    - the current user (optional)
    - the current application (optional)

    :param include_user_context:
        Whether the cache key should contain a value uniquely identifying the current user.
    :param include_application_context:
        Whether the cache key should contain a value uniquely identifying the current application.
    :return: 64 character string of hexadecimal digits
    """
    # Use the current Git revision hash to make the cache keys differ after a code deployment
    context = dict(version=current_app.config.get('GIT_REVISION', ''))

    if include_user_context:
        if g.user:
            context['current_user_id'] = g.user.id

        if g.real_user:
            context['real_user_id'] = g.real_user.id

    if include_application_context:
        if g.application:
            context['application_id'] = g.application.id

    return _create_response_data_cache_key(request, **context)


def cache_response_data_fn(fn, region, key, *args, **kwargs):
    include_user_context = not kwargs.pop('ignore_user_context', False)
    include_application_context = not kwargs.pop('ignore_application_context', False)

    use_cache = _can_use_response_data_cache()

    if use_cache:
        cache_region = dogpile_cache.get_region(region)
        cache_key = _generate_response_data_cache_key(
            include_user_context=include_user_context,
            include_application_context=include_application_context) if key is None else key

        rv = cache_region.get(cache_key)
        if rv is not NO_VALUE:
            return rv

    rv = fn(*args, **kwargs)

    if use_cache:
        cache_region.set(cache_key, rv)

    return rv
