import re

from enum21 import Enum
from marshmallow import Schema, fields
from sqlalchemy import orm

from ct_core_api.common import class_utils as cu, string_utils as su


def _make_enum_item_name(value, prefix=''):
    """Create a Python-safe name for an `EnumItem`.
    :param value: The value representing the `EnumItem` name.
    :return: A capitalized, snake-cased string with non-alphanumeric characters removed.
    """
    return prefix + su.camel_to_snake(re.sub(r'\W+', '', str(value))).upper()


def is_enum_type(cls):
    """True if this `cls` is an `Enum` or one of its subclasses (ie. `DynamicEnum`), False otherwise."""
    return hasattr(cls, '_item_dict')


def is_dynamic_enum(cls):
    """True if this `cls` is a `DynamicEnum`, False otherwise."""
    return hasattr(cls, '__enum_items__')


def create_enum_item_proxy(name=None, key=None, value=None, metadata=None):
    """Create a dictionary representing the `EnumItem` attributes. Useful for serialization."""
    if metadata:
        # Filter out complex types that may not be JSON serializable
        metadata = {k: v for k, v in metadata.items() if not hasattr(v, '__dict__')}
    metadata = metadata or None
    return dict(name=name, key=key, value=value, metadata=metadata)


def create_enum_proxy(name, enum_proxy_items, metadata=None):
    """Create a dictionary representing an `Enum` and its `EnumItem` members.
    Useful for serialization.
    :param name: The name of the `Enum`.
    :param enum_proxy_items: A list of `EnumItem` proxy dicts.
    :param metadata: A dict of metadata for this `Enum`.
    """
    return dict(name=name, items=enum_proxy_items, metadata=metadata)


def get_all_enum_proxies():
    """Produce a collection of all the application Enums (subclasses of `Enum`) in proxy form.

    Note: Subclasses of `Enum` will only be found if they were previously imported.
    :return: A list of dicts of the form::
        {
            'name': <Enum.__name__>,
            'items: [
                {
                    'name': <EnumItem.name>,
                    'key': <EnumItem.key>,
                    'value': <EnumItem.value>,
                    'metadata': <EnumItem.metadata>,
                },
            ],
            'metadata': {...},
        }
    """
    enum_proxies = []
    for enum_cls in sorted(cu.subclasses(Enum), key=lambda obj: obj.__name__):
        if is_dynamic_enum(enum_cls):
            # Explicitly refresh the dynamic enums
            enum_cls.__refresh__()

        items = [create_enum_item_proxy(
            su.snake_to_spinal(enum_cls.lookup(x[0])), x[0], x[1], enum_cls.metadata(x[0])) for x in enum_cls.verbose()]

        enum_metadata = enum_cls.__metadata__ if hasattr(enum_cls, '__metadata__') else None

        enum_proxies.append(create_enum_proxy(enum_cls.__name__, items, enum_metadata))
    return enum_proxies


def extract_enum_items_by_attribute(model_cls, key_attr, name_attr, value_attr):
    """Extract `Enum` proxy objects from a model.
    :param model_cls: The `Model` class.
    :param key_attr: The name of the `Model` attribute that represents the `EnumItem` key.
    :param name_attr: The name of the `Model` attribute that represents the `EnumItem` name.
    :param value_attr: The name of the `Model` attribute that represents the `EnumItem` value.
    :return: A list of Enum proxy objects.
    """
    def make_enum_item_name(value):
        if isinstance(value, (str, unicode)):
            return _make_enum_item_name(value)
        # EnumItem names must be valid Python identifiers, so prefix non-string values with an "E"
        return _make_enum_item_name(value, prefix='E')

    class EnumItemSchema(Schema):
        key = fields.Integer(attribute=key_attr)
        name = fields.Function(lambda obj: make_enum_item_name(getattr(obj, name_attr)))
        value = fields.String(attribute=value_attr)

    return [create_enum_item_proxy(**item) for item in EnumItemSchema(many=True).
            dump(model_cls.query.options(orm.load_only(key_attr, name_attr, value_attr)).all()).data]


def enum_item_repr(enum_cls, key):
    return "e.{}.{}".format(enum_cls.__name__, enum_cls.lookup(key))
