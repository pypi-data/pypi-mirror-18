import logging

from flask_restplus import fields as restplus_fields
from flask_restplus.utils import merge

from ct_core_api.api.core.schema import ma

_logger = logging.getLogger(__name__)


class APIModelProxy(object):
    """A proxy for a Swagger API model class.
    Contains the name of the Swagger model.
    """
    def __init__(self, name):
        self.__apidoc__ = dict(name=name)


def create_restplus_fields_from_marshmallow_schema(schema):
    """Create a dict of field names to Restplus fields from a Marshmallow schema.
    :param schema: A Marshmallow :class:`Schema` instance.
    :return: A dict of field names to Restplus fields.
    """
    return {k: create_restplus_field_from_marshmallow_field(v) for k, v in schema._update_fields().iteritems()}


def create_restplus_field_from_marshmallow_field(field, _nested_field_name=None):
    """Create a Restplus field from a Marshmallow field.
    The Restplus field contains the API documentation and metadata necessary to generate the Swagger documentation.
    :param field: A Marshmallow :class:`Field` instance.
    :param _nested_field_name: A derived name for the nested field -- for internal use only.
    :return: A Restplus field derived from its base `Raw` class.
    """
    def field_kwargs(f, *attrs):
        kwargs = {}
        for attr in attrs:
            if isinstance(attr, tuple):
                a, k = attr
            else:
                a = k = attr
            try:
                value = getattr(f, a)
            except AttributeError:
                value = f.metadata.get(a)
            kwargs[k] = value
        return kwargs

    def merge_apidoc(from_field, to_field):
        if hasattr(from_field, '__apidoc__'):
            to_field.__apidoc__ = merge(getattr(to_field, '__apidoc__', {}), from_field.__apidoc__)

    if not hasattr(field, '__apidoc__'):
        field.__apidoc__ = {}

    restplus_field = None
    restplus_cls = None
    restplus_attrs = ['attribute', 'default', 'description', 'required']  # default attrs

    if isinstance(field, ma.Arbitrary):
        restplus_cls = restplus_fields.Arbitrary
        restplus_attrs += ['min', 'max']
    elif isinstance(field, (ma.ExternalId, ma.Html)):
        restplus_cls = restplus_fields.String
    elif isinstance(field, (ma.Select, ma.Enum)):
        restplus_cls = restplus_fields.String
        restplus_attrs += [('choices', 'enum')]
    elif isinstance(field, ma.Fixed):
        restplus_cls = restplus_fields.Fixed
        restplus_attrs += ('min', 'max', 'decimals')
    elif isinstance(field, ma.Float):
        restplus_cls = restplus_fields.Float
        restplus_attrs += ['min', 'max']
    elif isinstance(field, ma.FormattedString):
        restplus_cls = restplus_fields.FormattedString
        restplus_attrs += ['min', 'max', 'src_str']
    elif isinstance(field, ma.Integer):
        restplus_cls = restplus_fields.Integer
        restplus_attrs += ['min', 'max']
    elif isinstance(field, ma.List):
        container_field = field.container
        merge_apidoc(field, container_field)
        restplus_field = restplus_fields.List(
            create_restplus_field_from_marshmallow_field(container_field),
            **field_kwargs(field, *restplus_attrs))
    elif isinstance(field, ma.Nested):
        nested = field.nested
        # Marshmallow supports self-referential nested fields by using the `self` identifier.
        if nested == 'self':
            # In this case, the nested field's schema class will be the same as its parent class
            nested = field.parent.__class__
            _nested_field_name = _nested_field_name or nested.resolve_schema_name()

        # Support Swagger array type documentation
        field.__apidoc__ = merge(field.__apidoc__, {'as_list': field.many})

        nested_proxy = APIModelProxy(_nested_field_name or field.schema_name)
        restplus_cls = restplus_fields.Nested
        restplus_attrs = ('attribute', 'default', 'allow_null')  # set attrs explicitly
        restplus_field = restplus_fields.Nested(nested=nested_proxy, **field_kwargs(field, *restplus_attrs))
    elif isinstance(field, ma.Raw):
        restplus_cls = restplus_fields.Raw
    elif isinstance(field, ma.Url):
        restplus_cls = restplus_fields.Url
        restplus_attrs += ('endpoint', 'absolute', 'scheme')
    elif isinstance(field, (ma.Function, ma.Method)):
        if field.return_field is not None:
            return_field = field.return_field
            merge_apidoc(field, return_field)
            _nested_field_name = field.return_field.schema.resolve_schema_name(field.schema_view) \
                if isinstance(field.return_field, ma.Nested) else None
            return create_restplus_field_from_marshmallow_field(return_field, _nested_field_name)
        restplus_cls = restplus_fields.Raw
    else:
        try:
            field_name = field.__class__.__name__
            restplus_cls = getattr(restplus_fields, field_name)
        except AttributeError:
            # logger.warn(
            #     "Unable to convert Marshmallow field to Restplus field. Unsupported type: {}".format(field_name))
            restplus_cls = restplus_fields.String

    if restplus_field is None:
        restplus_field = restplus_cls(**field_kwargs(field, *restplus_attrs)) if restplus_cls else None

    # Denote deprecated fields
    if 'deprecated' in field.metadata:
        field.__apidoc__['deprecated'] = field.metadata['deprecated']

    # Include additional documentation metadata based on field type
    if isinstance(field, ma.Enum):
        field.__apidoc__['enum_cls'] = field.enum_cls
    elif isinstance(field, ma.Html):
        field.__apidoc__['has_html'] = True

    # Copy Swagger documentation over to restplus field
    if hasattr(field, '__apidoc__'):
        restplus_field.__apidoc__ = field.__apidoc__

    return restplus_field
