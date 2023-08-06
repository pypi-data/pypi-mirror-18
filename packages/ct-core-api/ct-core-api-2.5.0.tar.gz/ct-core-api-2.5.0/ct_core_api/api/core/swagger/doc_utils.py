from flask_principal import Permission
from flask_restplus.utils import merge

from ct_core_api.api.common import api_helpers as ah
from ct_core_api.api.core import search, swagger
from ct_core_api.api.core.auth import CompositeOrPermission


########################################
# Documentation Params
########################################

DEFAULT_SEARCH_TERM_LABEL = '[default search term]'


def doc_param_id(name='id', resource_name=None, required=True):
    description = u"The {} identifier.".format(resource_name or 'resource')
    return swagger.doc_param(name, description, required=required)


def doc_param_selectors(name=search.SearchConfig.FIELD_SELECTORS_PARAM, description=None, required=None):
    if description is None:
        description = u"Describes which fields will be included in resource response."
    return swagger.doc_param(name, description, required=required)


def doc_param_search_query(name=search.SearchConfig.SEARCH_QUERY_PARAM, search_params_doc=None, required=None):
    description = u"The search query."
    if search_params_doc is not None:
        description += u"<br>".join([
            u"<dt>{}:</dt><dd>{}</dd>".format(k or DEFAULT_SEARCH_TERM_LABEL, v)
            for k, v in sorted(search_params_doc.items())])
    return swagger.doc_param(name, description, required=required)


def _doc_permission(permission):
    if isinstance(permission, Permission):
        return permission.__class__.__name__
    if isinstance(permission, CompositeOrPermission.Doc):
        return str(permission)
    return permission.__name__


def doc_permissions(*permissions):
    return [_doc_permission(permission) for permission in permissions]


def doc_response_permissions(*permissions):
    required_perms = u" <br>Required permission(s): <br>{}".format(
        ' AND <br>'.join(doc_permissions(*permissions))) if permissions else ''
    return dict(responses={403: u"Permission denied.{}".format(required_perms)})


########################################
# Documentation Helpers
########################################

def _resolve_schema_name(schema, schema_view=None):
    if isinstance(schema, (str, unicode)):
        return schema
    return schema.resolve_schema_name(schema_view)


def _resolve_params(params_list=None, parser_list=None):
    params_list = params_list or []
    parser_params_list = [swagger.parser_to_params(parser) for parser in parser_list] if parser_list else []
    # Params earlier in the list will have their keys overwritten by the params that follow them.
    return reduce(lambda x, y: dict(x.items() + y.items()), parser_params_list + params_list, {})


def doc_endpoint(
        fn_name,
        fn_args,
        schema=None,
        schema_view=None,
        description=None,
        search_parsers=None,
        search_params_doc=None,
        parser=None,
        params=None,
        permissions=None,
        is_collection=None,
        **kwargs):
    """
    Generate a Swagger 2.0 compliant documentation dict that describes an API endpoint operation and its parameters.
    :param fn_name: The name of the `APIResource`'s method that implements this operation.
    The naming of this method is used to derive the container type of the return value.
    :param fn_args: A list of the parameter names for the `APIResource`'s method.
    :param schema: The `APISchema` class representing the Swagger response model.
    :param schema_view: The name of the schema view for this `schema`, optional.
    It's combined with the `schema`'s name to form the name of the Swagger model.
    :param description: A description of this API operation that will be shown as "Implementation Notes", optional.
    :param search_parsers: One or more search related parsers describing the operation's input parameters, optional.
    :param search_params_doc: A documentation dict describing the components of a search query string, optional.
    :param parser: The parser describing the operation's input parameters, optional.
    :param params: An explicit list of Swagger documentation input params to include alongside the others.
    :param permissions: One or more `Permission`s describing the `Need`s of this operation, optional.
    See `doc_response_permissions`.
    :param is_collection: The Swagger response is represented as a collection of models if True or as a single model
    if False. The default is `None` which means the collection type will be derived from `fn_name`.
    :param kwargs: A dict of additional information to merge into the final documentation dict.
    :return: The final documentation dict
    """
    params_list = []
    parser_list = []

    schema_model = None

    if schema:
        # Resolve the schema model name, taking the schema view into account.
        schema_model = _resolve_schema_name(schema, schema_view)

        # Determine if the response is a single model or a collection of them
        # If a collection, the name of the schema model will put into a list so that Swagger knows its an array.
        if is_collection is not None:
            schema_model = [schema_model] if is_collection else schema_model
        elif '_many' in fn_name or '_all' in fn_name:
            schema_model = [schema_model]

    # Accumulate the common params for this resource endpoint
    if 'id' in fn_args:
        params_list.append(doc_param_id())

    if search.SearchConfig.FIELD_SELECTORS_PARAM in fn_args:
        params_list.append(doc_param_selectors())

    if search_params_doc:
        params_list.append(doc_param_search_query(search_params_doc=search_params_doc))

    if params:
        params_list.append(params)

    # Accumulate the common parsers for this resource endpoint
    if search_parsers:
        parser_list.extend(search_parsers)

    if parser:
        parser_list.append(parser)

    # Resolve all parser params and combine them with the others to create a single params dict
    params = _resolve_params(params_list=params_list, parser_list=parser_list)

    # Build the final documentation dict
    doc = dict(model=schema_model) if schema_model else dict()
    # doc['id'] = fn_name  # Use the function's name as the operation's identifier (this value is also the "action")

    if params:
        doc['params'] = params

    if description:
        doc['description'] = description

    doc.update(kwargs)

    if permissions:
        doc['permissions'] = doc_permissions(*permissions)

        # Recursively merge the response permissions into the documentation dict
        doc = merge(doc, doc_response_permissions(*permissions))

    return doc


def parse_api_resource_operation_info(resource_entry, include_params=False):
    """Return a dict containing useful facts about a resource operation.
    Information will be parsed from the API's internal representation of a resource entry and from
    documentation metadata on the resource's method.
    """
    resource = resource_entry[0].resource_name() \
        if hasattr(resource_entry[0], 'resource_name') else resource_entry[0].__name__
    endpoint = resource_entry[2]['endpoint'].split('|')[-1]
    method = (resource_entry[2]).get('methods', [''])[0].upper()
    url = resource_entry[1][0]

    api_doc = getattr(getattr(resource_entry[0], endpoint, None), '__apidoc__', {})

    is_deprecated = bool(api_doc.get('deprecated'))
    deprecated_removal_date = api_doc.get('deprecated_removal_date')
    deprecated_on_date = api_doc.get('deprecated_on_date')
    permissions = api_doc.get('permissions', [])
    params = api_doc.get('params', {}) if include_params else None

    return dict(
        resource=resource,
        endpoint=endpoint,
        method=method,
        url=url,
        params=params,
        is_deprecated=is_deprecated,
        deprecated_removal_date=deprecated_removal_date,
        deprecated_on_date=deprecated_on_date,
        permissions=permissions)


def parse_enum_ids(resources, schema_models):
    """Return the set of all the external enum identifiers that are referenced by this API.
    This includes the enums used in operation input parameters and those present in the schema response models.
    """
    enum_ids = set()
    # Extract the enum identifiers from the operation parameters
    for resource_entry in resources:
        operation_info = parse_api_resource_operation_info(resource_entry, include_params=True)
        for p in operation_info['params'].itervalues():
            enum_ids.add(p.get('x-enum-type'))
    # Extract the enum identifiers from the schema models
    for model_entry in schema_models.itervalues():
        for field in model_entry.itervalues():
            if hasattr(field, '__apidoc__') and 'enum_cls' in field.__apidoc__:
                enum_ids.add(ah.enum_id(field.__apidoc__['enum_cls']))
    enum_ids.discard(None)
    enum_ids.discard('')
    return enum_ids
