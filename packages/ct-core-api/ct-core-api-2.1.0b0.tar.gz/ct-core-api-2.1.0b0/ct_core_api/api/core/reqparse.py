import logging
from datetime import datetime
from functools import partial
from simplejson import JSONDecodeError
from urlparse import urlparse

import validation21 as vv
from flask_restful import abort, reqparse
from marshmallow.exceptions import ValidationError
from werkzeug import routing

from ct_core_api import api
from ct_core_api.api.common import api_helpers as ah, json_utils as ju
from ct_core_api.common import datetime_utils as dtu, enum_utils as eu, string_utils as su

_logger = logging.getLogger(__name__)


########################################
# URL Type Conversions
########################################

class ExternalIdURLConverter(routing.BaseConverter):
    """Convert an external identifier in the URL from its hex-string form to its native int value."""
    def to_python(self, value):
        if not ah.is_valid_external_id(value):
            err_msg = 'Invalid external identifier'
            _logger.error(err_msg, extra={'value': value})
            error = routing.ValidationError(err_msg)
            error.args += (value,)
            raise error

        try:
            return ah.from_external_id(value)
        except ValueError:
            # Catch conversion errors so that the error handler can generate an appropriate response
            pass

    def to_url(self, obj):
        return ah.to_external_id(obj)


########################################
# Custom Argument Types
########################################

class ExternalId(int):
    """Convert an "external" eight character hexadecimal string to an "internal" integer identifier."""
    def __new__(cls, value):
        return ah.from_external_id(value)


class DateTimeUTC(datetime):
    """A UTC `datetime` object that handles string conversions."""
    def __new__(cls, value):
        dt = vv.DateTime().to_python(value)
        if dt is not None:
            return dtu.make_naive_datetime(dt)  # Need to remove tzinfo for db storage


class JSONObject(object):
    """An object loaded from a JSON string."""
    def __new__(cls, value):
        try:
            obj = ju.loads(value)
        except (JSONDecodeError, TypeError):
            raise ValueError('Invalid JSON string')
        return obj


def json_object_argument_help_example(help_text, example_json):
    """Return a Swagger UI compliant HTML string containing the help text for a `JSONObject` argument.
    The `example_json` is styled as a formatted code snippet.
    """
    return (
        "{}:<br>"
        "<div class='snippet_json' style='display: block;'>"
        "<pre style='overflow: scroll; width: 150px;'><code>{}</code></pre></div>".format(help_text, example_json))


class UnicodeEmail(unicode):
    """A unicode string that performs email address validation on instantiation."""
    def __new__(cls, value):
        value = vv.Email().to_python(value)
        if isinstance(value, (str, unicode)):
            return super(UnicodeEmail, cls).__new__(cls, value)


class UnicodeNoHTML(unicode):
    """A unicode string that performs HTML sanitization on instantiation.
    The input will have all HTML removed and the HTML entities unescaped.
    """

    def __new__(cls, value):
        value = su.clean_html(value, allowed_tags=[], allowed_attrs={}, markup=False)
        value = su.unescape_entities(value)
        obj = super(UnicodeNoHTML, cls).__new__(cls, value)
        return obj


class UnicodeHTML(unicode):
    """A unicode string that performs HTML sanitization on instantiation.
    The input will have all non-white-listed HTML elements and attributes removed.
    """

    @staticmethod
    def _filter_anchor_attributes(name, value):
        if name in {'title', 'target', 'rel'}:
            return True
        elif name == 'href':
            p = urlparse(value.strip())
            return p.scheme in {'', 'ftp', 'http', 'https', 'mailto'}
        return False

    def __new__(cls, value):
        allowed_tags = su.DEFAULT_ALLOWED_HTML_TAGS
        allowed_attrs = {
            'a': cls._filter_anchor_attributes,
            'abbr': ['title'],
            'acronym': ['title'],
        }

        value = su.clean_html(value, allowed_tags=allowed_tags, allowed_attrs=allowed_attrs, markup=False)
        obj = super(UnicodeHTML, cls).__new__(cls, value)
        return obj


########################################
# Arguments
########################################

class ArgumentErrorType(object):
    CHOICE = 'choice'
    INVALID = 'invalid'
    REQUIRED = 'required'
    TYPE = 'type'
    UNKNOWN = 'unknown'


class ArgumentValidationException(ValueError):
    def __init__(self, arg_name, message, type_):
        self.arg_name = arg_name
        self.message = message
        self.type = type_


class Argument(reqparse.Argument):
    def __init__(self, *args, **kwargs):
        self.validator = kwargs.pop('validator', None)
        self.metadata = kwargs.pop('metadata', {})
        super(Argument, self).__init__(*args, **kwargs)

        self.choices = list(self.choices)  # Use a list instead of tuple for easier management
        self.metadata[api.DocumentationMetadata.DEPRECATED] = kwargs.pop('deprecated', False)

        if eu.is_enum_type(self.type):
            enum_id = ah.enum_id(self.type)

            self.help = "{}: {}".format('Dynamic Enum' if eu.is_dynamic_enum(self.type) else 'Enum', enum_id)

            # Set the choices if the argument type is an Enum and explicit choices were not provided.
            # Note: Choices are validated after type conversion occurs.
            if not self.choices and not eu.is_dynamic_enum(self.type):
                self.choices = self.type.keys()

            if self.choices:
                # Store the external Enum identifier strings for Swagger documentation
                self.metadata[api.DocumentationMetadata.ENUM_CHOICES] = ah.enum_choices_for_keys(self.type, *self.choices)

                # None is a valid choice if the argument isn't required and it appears in the request
                if not self.required and not self.store_missing:
                    self.choices.append(None)
        elif self.type is UnicodeHTML:
            self.metadata[api.DocumentationMetadata.HAS_HTML] = True
        elif self.type is JSONObject:
            self.metadata[api.DocumentationMetadata.HAS_JSON] = True

    def convert(self, value, op):
        if eu.is_enum_type(self.type):
            # Fetch the `EnumItem` key for this `EnumItem` identifier
            converted_value = ah.enum_item_key(self.type, value) if value else None
        elif self.type is bool:
            # Convert truthy or falsey string values to a bool
            converted_value = vv.Boolean().to_python(value)
        else:
            # Otherwise, perform the default type conversion
            converted_value = super(Argument, self).convert(value, op)

        if isinstance(converted_value, (str, unicode)):
            if converted_value.strip() == '':
                converted_value = None

        # Raise an error if a required argument has no value post-conversion
        if self.required and converted_value is None:
            if isinstance(self.location, (str, unicode)):
                error_msg = u"Missing required parameter {0} in {1}".format(
                    self.name,
                    reqparse._friendly_location.get(self.location, self.location))
            else:
                friendly_locations = [reqparse._friendly_location.get(loc, loc) for loc in self.location]
                error_msg = u"Missing required parameter {0} in {1}".format(
                    self.name,
                    ' or '.join(friendly_locations))
            raise ValueError(error_msg)

        if hasattr(self.validator, '__call__'):
            self.validator(converted_value)

        return converted_value

    @classmethod
    def raise_validation_error(cls, arg_name, message, error_type):
        abort(422, params={arg_name: dict(message=message, error=error_type)})

    def handle_validation_error(self, error):
        arg_name = self.name
        error_str = str(error)
        error_type = ArgumentErrorType.UNKNOWN
        error_message = self.help if self.help is not None else error_str

        if isinstance(error, ArgumentValidationException):
            arg_name = error.arg_name
            error_message = error.message
            error_type = error.type
        elif isinstance(error, (ValueError, vv.ValidationException)):
            if 'required' in error_str:
                error_type = ArgumentErrorType.REQUIRED
            elif 'choice' in error_str:
                error_type = ArgumentErrorType.CHOICE
            else:
                error_type = ArgumentErrorType.INVALID
        elif isinstance(error, TypeError):
            error_type = ArgumentErrorType.TYPE

        self.raise_validation_error(arg_name, error_message, error_type)


########################################
# Argument Validator Functions
########################################

def len_validator(min_len=0, max_len=None):
    def validator(value):
        try:
            length = len(value)
        except TypeError:
            length = -1

        if min_len is not None and length < min_len:
            raise ValueError("Invalid length: {}, minimum: {}".format(length, min_len))
        elif max_len is not None and length > max_len:
            raise ValueError("Invalid length: {}, maximum: {}".format(length, max_len))
    return validator


def range_validator(min_value=None, max_value=None):
    def validator(value):
        if min_value is not None and value < min_value:
            raise ValueError("Invalid value: {}, minimum: {}".format(value, min_value))
        elif max_value is not None and value > max_value:
            raise ValueError("Invalid value: {}, maximum: {}".format(value, max_value))
    return validator


def json_object_validator(schema, argument_name):
    """Validate a `JSONObject` argument's value using the provided schema instance.
    :raises: ArgumentValidationException
    """
    schema.strict = False
    return partial(deserialize_dict_with_schema, schema=schema, arg_name=argument_name)


def deserialize_dict_with_schema(value, schema, arg_name):
    """Deserializes a dict with the given schema.

    :param value: Input dict
    :param schema: Marshmallow schema. Recommend setting ``strict`` to ``False``, or we can't customize error handling.
    :param arg_name: Name of the field we're validating
    :returns Deserialized dict
    :raises ArgumentValidationError
    """
    parsed_data = {}
    error_data = {}

    try:
        parsed_data, errors = schema.load(value)
        if errors:
            # Only reveal one error at a time, starting with the first
            first_error = errors.items()[0]
            first_error_arg_name = first_error[0]
            first_error_message = first_error[1][0]
            # Create fully-qualified argument name
            full_arg_name = '.'.join([arg_name, first_error_arg_name])

            error_data = dict(
                arg_name=full_arg_name, message=first_error_message, type_=ArgumentErrorType.INVALID)
    except ValidationError as exc:
        error_data = dict(arg_name=arg_name, message=exc.message, type_=ArgumentErrorType.INVALID)

    if error_data:
        raise ArgumentValidationException(**error_data)
    return parsed_data


class JSONDeserializerType(object):
    """Deserializes JSON as the ``type`` parameter of an ``Argument``.

    ...yes, it's an instance, not a type, but ``Argument`` just needs a callable, so eh.
    """
    def __init__(self, schema):
        self.schema = schema
        self.schema.strict = False

    def __call__(self, value, name):
        dict_to_deserialize = JSONObject(value)
        return deserialize_dict_with_schema(dict_to_deserialize, self.schema, name)


########################################
# Request Parsers
########################################

class RequestParser(reqparse.RequestParser):
    def __init__(self, argument_class=Argument, namespace_class=reqparse.Namespace):
        super(RequestParser, self).__init__(argument_class=argument_class, namespace_class=namespace_class)

    # TODO: Decide if we want to abort with a bad request if there were un-parsed args in the request
    def parse_args(self, req=None, strict=False):
        return super(RequestParser, self).parse_args(req=req, strict=strict)


# ======================================
# Pagination Request Parser
# ======================================

class PaginationConfig(object):
    OFFSET_PARAM = 'offset'
    LIMIT_PARAM = 'limit'

    DEFAULT_LIMIT = 100
    DEFAULT_OFFSET = 0


class PaginationRequestParser(RequestParser):
    def __init__(self, *args, **kwargs):
        self.limit_only = kwargs.pop('limit_only', False)
        super(PaginationRequestParser, self).__init__(*args, **kwargs)

        if not self.limit_only:
            self.add_argument(
                PaginationConfig.OFFSET_PARAM, type=int, default=PaginationConfig.DEFAULT_OFFSET, location='args')

        self.add_argument(
            PaginationConfig.LIMIT_PARAM, type=int, default=PaginationConfig.DEFAULT_LIMIT, location='args')

    def _parse_offset(self, args):
        offset = getattr(args, PaginationConfig.OFFSET_PARAM, PaginationConfig.DEFAULT_OFFSET)
        if offset < 0:
            offset_arg = next((arg for arg in self.args if arg.name == PaginationConfig.OFFSET_PARAM), None)
            offset_arg.raise_validation_error(
                PaginationConfig.OFFSET_PARAM, u'Invalid offset', ArgumentErrorType.INVALID)
        return offset

    def _parse_limit(self, args, max_limit=None):
        limit = getattr(args, PaginationConfig.LIMIT_PARAM, PaginationConfig.DEFAULT_LIMIT)
        if limit < 0:
            limit_arg = next((arg for arg in self.args if arg.name == PaginationConfig.LIMIT_PARAM), None)
            limit_arg.raise_validation_error(
                PaginationConfig.LIMIT_PARAM, u'Invalid limit', ArgumentErrorType.INVALID)

        if max_limit and limit > max_limit:
            limit = max_limit

        return limit

    def parse_limit(self, max_limit=None):
        args = self.parse_args()
        return self._parse_limit(args, max_limit=max_limit)

    def parse_offset_limit(self, max_limit=None):
        args = self.parse_args()

        offset = self._parse_offset(args) if not self.limit_only else None
        limit = self._parse_limit(args, max_limit=max_limit)

        return offset, limit

pagination_parser = PaginationRequestParser()


# ======================================
# Sort/Order Request Parser
# ======================================

class SortConfig(object):
    SORT_PARAM = 'sort'
    ORDER_PARAM = 'order'
    ORDER_ASC = 'asc'
    ORDER_DESC = 'desc'

    DEFAULT_ORDER = ORDER_DESC
    DEFAULT_SORT = None
    DEFAULT_ORDER_CHOICES = [ORDER_ASC, ORDER_DESC]
    DEFAULT_SORT_CHOICES = []


class SortOrderRequestParser(RequestParser):
    def __init__(self, *args, **kwargs):
        sort_default = kwargs.pop('sort_default', SortConfig.DEFAULT_SORT)
        sort_choices = kwargs.pop('sort_choices', SortConfig.DEFAULT_SORT_CHOICES)

        order_default = kwargs.pop('order_default', SortConfig.DEFAULT_ORDER)
        order_choices = kwargs.pop('order_choices', SortConfig.DEFAULT_ORDER_CHOICES)

        super(SortOrderRequestParser, self).__init__(*args, **kwargs)

        self.add_argument(
            SortConfig.SORT_PARAM,
            type=str,
            location='args',
            default=sort_default,
            choices=sort_choices)

        self.add_argument(
            SortConfig.ORDER_PARAM,
            type=str,
            location='args',
            default=order_default,
            choices=order_choices)

    def parse_sort_order(self):
        args = self.parse_args()
        return args.get(SortConfig.SORT_PARAM), args.get(
            SortConfig.ORDER_PARAM)


sort_order_parser = SortOrderRequestParser()


# ======================================
# Aggregation Parser
# ======================================

class AggregationConfig(object):
    AGGREGATION_TYPE_PARAM = 'aggregation_type'
    AGGREGATION_TYPE_PER_FIELD_INCLUSIVE = 'per_field_inclusive'

    AGGREGATION_TYPE_CHOICES = [AGGREGATION_TYPE_PER_FIELD_INCLUSIVE, ]
    DEFAULT_AGGREGATION_TYPE = None


class AggregationRequestParser(RequestParser):
    def __init__(self, *args, **kwargs):
        super(AggregationRequestParser, self).__init__(*args, **kwargs)

        self.add_argument(
            AggregationConfig.AGGREGATION_TYPE_PARAM,
            type=str,
            default=AggregationConfig.DEFAULT_AGGREGATION_TYPE,
            location='args',
            choices=AggregationConfig.AGGREGATION_TYPE_CHOICES)

    def parse_aggregation(self):
        args = self.parse_args()
        return args.get(AggregationConfig.AGGREGATION_TYPE_PARAM)

aggregation_parser = AggregationRequestParser()


# ======================================
# Pagination Sort/Order Parser
# ======================================

class PaginationSortOrderRequestParser(PaginationRequestParser, SortOrderRequestParser):
    def __init__(self, *args, **kwargs):
        super(PaginationSortOrderRequestParser, self).__init__(*args, **kwargs)

pagination_sort_order_parser = PaginationSortOrderRequestParser()
