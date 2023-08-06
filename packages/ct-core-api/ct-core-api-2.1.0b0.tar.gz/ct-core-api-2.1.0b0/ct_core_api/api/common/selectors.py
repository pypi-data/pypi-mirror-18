import re

from ct_core_api.common import string_utils as su

NO_INNER_PARENS = re.compile(r'\([a-zA-Z_,]*\)')
RESOURCE_FIELDS_RE = re.compile(r'^:\w*\((.*)\)$')
SUBRESOURCE_FIELDS_RE = re.compile(r'(\w+):\(([\w,]+)\)')
MODIFIERS_RE = re.compile(r'(\w*):(\w+)')


class FieldSelectors(object):
    def __init__(self, *fields, **sub_fields):
        self.fields = list(fields)
        self.sub_fields = sub_fields

    @property
    def all_field_names(self):
        return self.fields + self.sub_fields.keys()

    @property
    def sub_field_names(self):
        return self.sub_fields.keys()

    def __contains__(self, f):
        return f in self.all_field_names

    def __repr__(self):
        return "{}({!r}, {!r})".format(self.__class__.__name__, list(self.fields), self.sub_fields)

    @classmethod
    def from_str(cls, value):
        """Create `FieldSelectors` from a string representation of the fields and sub-fields.

        >>> FieldSelectors.from_str(':(name,business_user:(first_name,business_profile:(primary_industry))')
        FieldSelectors(['name'], {'business_user': FieldSelectors(['first_name'], {'business_profile': FieldSelectors(['primary_industry'], {})})})
        """
        delimiters = ',:()'

        fs = FieldSelectors()
        field_name = None
        stack = []

        for token in su.tokenize(value, *delimiters):
            if token in delimiters:
                if field_name is not None:
                    if token == ':':
                        stack.append(fs)
                    elif token == '(':
                        fs.sub_fields[field_name] = FieldSelectors()
                        fs = fs.sub_fields[field_name]
                    elif token in [',', ')']:
                        fs.fields.append(field_name)
                        field_name = None

                if token == ')' and stack:
                    fs = stack.pop()
            else:
                field_name = token

        return fs

    def to_dict(self):
        d = {k: None for k in self.fields}
        for k, v in self.sub_fields.iteritems():
            d[k] = v.to_dict()
        return d


class ResourceModifiers(object):
    def __init__(self, resource_modifier=None, **sub_resource_modifiers):
        self.resource_modifier = resource_modifier
        self.sub_resource_modifiers = sub_resource_modifiers

    def get_sub_resource_modifier(self, sub_resource, default=None):
        return self.sub_resource_modifiers.get(sub_resource, default)

    @property
    def sub_resource_names(self):
        return self.sub_resource_modifiers.keys()

    def __repr__(self):
        return "{}({!r}, {!r})".format(self.__class__.__name__, self.resource_modifier, self.sub_resource_modifiers)


def parse_selectors(selectors):
    # Locate top-level resource field values
    resource_fields_val = re.findall(RESOURCE_FIELDS_RE, selectors)
    # Remove the inner parenthesis
    resource_fields_val = re.sub(NO_INNER_PARENS, '', resource_fields_val[0]) if resource_fields_val else ''
    # Extract all the fields that don't contain a ':' (these are the sub-resource fields)
    resource_fields = filter(None, [f for f in resource_fields_val.split(',') if ':' not in f])
    # Extract a dict containing the comma-delimited sub-resource fields
    sub_resource_fields = {f: v.split(',') for f, v in re.findall(SUBRESOURCE_FIELDS_RE, selectors)}
    # Extract the resource and sub-resource modifiers
    modifiers = dict(re.findall(MODIFIERS_RE, selectors))
    resource_modifier, subresource_modifiers = modifiers.pop('', None), modifiers
    # Return the field selectors and resource modifiers
    return (FieldSelectors(*resource_fields, **sub_resource_fields),
            ResourceModifiers(resource_modifier, **subresource_modifiers))


selectors_param = dict(
    name="selectors",
    description="Specifies which fields are included in the resource response.",
    required=True,
    allowMultiple=False,
    dataType='string',
    paramtype='path')
