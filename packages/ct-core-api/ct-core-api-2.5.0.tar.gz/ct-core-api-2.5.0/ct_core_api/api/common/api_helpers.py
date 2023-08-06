import re

from flask import Blueprint, request

from ct_core_api.api.common import json_utils as ju
from ct_core_api.api.lib import opaque
from ct_core_api.common import string_utils as su


########################################
# Request Helpers
########################################

def get_user_agent_summary():
    user_agent = request.user_agent
    if user_agent:
        return ' '.join((user_agent.platform, user_agent.browser, user_agent.version))


def get_remote_addr():
    return list(request.access_route)[0] if request.access_route else None


########################################
# Response Helpers
########################################

def extract_response_text(resp):
    return resp.get_data(as_text=True)


def extract_response_json(resp):
    text = resp if isinstance(resp, (str, unicode)) else extract_response_text(resp)
    return ju.loads(text)


########################################
# Registration Helpers
########################################

def register_api_resources(
        app,
        api_ext,
        pkg_path,
        pkg_name,
        api_namespace='api',
        blueprint_prefix='api',
        url_prefix='/api'):
    """Register all the API resources within a specified package to application blueprints.
    The `APINamespace` instance in each module is identified by `api_namespace`.
    The API extension's version is combined with the provided prefixes to generate the blueprint name and URL path.
    """
    import pkgutil
    from importlib import import_module

    # Register every resource in each module's `api` namespace
    for _, module_name, is_pkg in pkgutil.iter_modules(pkg_path):
        if not is_pkg:
            api_ext.add_namespace(
                getattr(import_module(".{}".format(module_name), package=pkg_name), api_namespace))

    # Register the api blueprint with the api and app
    bp_name = "{}-v{}".format(blueprint_prefix, api_ext.version)
    url_prefix = "{}/v{}".format(url_prefix, api_ext.version)
    bp = Blueprint(bp_name, __name__, url_prefix=url_prefix)
    api_ext.init_app(bp)
    app.register_blueprint(bp)


########################################
# Enum Helpers
########################################

def enum_id(enum_cls):
    """Retrieve the external identifier for an `Enum` or `DynamicEnum` class."""
    return enum_cls.__name__


def make_enum_item_id(enum_cls, item_name):
    """Create an external identifier for an `EnumItem` that is suitable to transmit to the API client."""
    return su.snake_to_spinal(item_name)


def parse_enum_item_name(enum_cls, item_id):
    """Parse an `EnumItem` name from the external id provided by the API client."""
    return su.spinal_to_snake(item_id, screaming=True)


def enum_item_id(enum_cls, key):
    """Retrieve the `EnumItem` identifier corresponding to this `Enum` class and key.
    :param enum_cls: An `Enum`.
    :param key: The key value identifying this `EnumItem` member.
    :return: A unique string identifier for this `EnumItem`.
    :raises: `KeyError` if the key lookup fails.
    """
    if isinstance(key, long):
        key = int(key)
    return make_enum_item_id(enum_cls, enum_cls.lookup(key))


def enum_item_key(enum_cls, enum_item_id):
    """Retrieve the `EnumItem` key corresponding to this `Enum` class and `EnumItem` identifier.
    :param enum_cls: An `Enum`.
    :param enum_item_id: The `EnumItem` identifier.
    :return: The key value for this `EnumItem` member.
    """
    return getattr(enum_cls, parse_enum_item_name(enum_cls, enum_item_id))


def enum_choices(enum_cls, exclude=None):
    """The valid external id string values for this `Enum`.
    Useful for validating incoming request parameters.
    :param enum_cls: An `Enum`.
    :param exclude: A collection of `EnumItem` key strings that should be excluded from the choices.
    :return: A list strings
    """
    return [
        make_enum_item_id(enum_cls, item_name)
        for item_key, item_name in enum_cls.items() if exclude is None or item_key not in exclude
    ]


def enum_choices_for_keys(enum_cls, *keys):
    """The valid external id string values for these `EnumItem` keys.
    :param enum_cls: An `Enum`.
    :param keys: A collection of `EnumItem` keys.
    :return: A list strings
    """
    return [enum_item_id(enum_cls, key) for key in keys]


def get_enum_key_for_verbose_value(enum_cls, verbose_value, case_insensitive=False):
    """
    Returns the enum key for the FIRST matching verbose value

    :param enum_cls: An Enum
    :param verbose_value: The value for reverse lookup
    :param case_insensitive: Whether to match case-insensitively
    :return: The key value for the Enum
    """
    if case_insensitive:
        verbose_value = verbose_value.lower()
    for enum_key, enum_verbose_value in enum_cls.verbose():
        if case_insensitive:
            enum_verbose_value = enum_verbose_value.lower()
        if enum_verbose_value == verbose_value:
            return enum_key
    return None


########################################
# External Id Helpers
########################################

class ExternalIdConverter(opaque.OpaqueEncoder):
    """Convert an external identifier to internal identifier and vice versa.
    External identifiers are eight character hexadecimal strings, internal identifiers are integers.
    """
    def __init__(self):
        super(ExternalIdConverter, self).__init__(0xa9bd97b3)  # Secret key acts as random seed

    def internal_to_external(self, internal_id):
        if internal_id is None:
            return None
        return self.encode_hex(internal_id)

    def external_to_internal(self, external_id):
        if external_id is None or external_id == '':
            return None
        return self.decode_hex(external_id)


external_id_converter = ExternalIdConverter()
to_external_id = external_id_converter.internal_to_external
from_external_id = external_id_converter.external_to_internal


EXTERNAL_IDENTIFIER_RE = re.compile(r'^[a-f0-9]{8}$', re.IGNORECASE)


def is_valid_external_id(value):
    """Determine if this value represents a valid external identifier.

    >>> is_valid_external_id('ABCDEF12')  # valid (hex, uppercase)
    True
    >>> is_valid_external_id('abcdef12')  # valid (hex, lowercase)
    True
    >>> is_valid_external_id(u'ABCDEF12')  # valid (hex, unicode, uppercase)
    True
    >>> is_valid_external_id(u'abcdef12')  # valid (hex, unicode, lowercase)
    True
    >>> is_valid_external_id('34567890')  # valid (hex, numeric)
    True
    >>> is_valid_external_id(None)  # invalid (non-str)
    False
    >>> is_valid_external_id(34567890)  # invalid (non-str)
    False
    >>> is_valid_external_id('oooooooo')  # invalid (non-hex)
    False
    >>> is_valid_external_id(u'\xc3\xa0bcdef12')  # invalid (non-hex)
    False
    >>> is_valid_external_id(u'abcdef123')  # invalid (hex, length)
    False
    >>> is_valid_external_id(u'abcdef1')  # invalid (hex, length)
    False
    """
    try:
        return bool(EXTERNAL_IDENTIFIER_RE.match(value))
    except TypeError:
        return False
    return False
