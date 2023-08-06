from inspect import isclass

from flask_restplus import swagger
from flask_restplus.namespace import unshortcut_params_description
from flask_restplus.swagger import Swagger as BaseSwagger, extract_path_params, fields, extract_path, not_none
from flask_restplus.utils import merge

from ct_core_api import api
from ct_core_api.api.core import cache
from ct_core_api.api.common import api_helpers as ah, json_utils as ju
from ct_core_api.common import enum_utils as eu


class CustomSwaggerAttribute(object):
    CACHE_REGION = 'x-cache-region'
    CACHE_REGION_EXPIRATION = 'x-cache-region-expiration'
    DEPRECATED = 'x-deprecated'
    DEPRECATED_ON_DATE = 'x-deprecated-on-date'
    DEPRECATED_REASON = 'x-deprecated-reason'
    DEPRECATED_REMOVAL_DATE = 'x-deprecated-removal-date'
    ENUM_TYPE = 'x-enum-type'
    HAS_HTML = 'x-has-html'
    HAS_JSON = 'x-has-json'
    PERMISSIONS = 'x-permissions'


# Capture the original Flask-Restplus functions
swagger.__parser_to_params = swagger.parser_to_params
swagger.__field_to_property = swagger.field_to_property


# Add Swagger param support for:
# - Enum choices
# - String arguments containing HTML or JSON
# - Deprecated arguments
# - Boolean defaults
def parser_to_params(parser):
    params = swagger.__parser_to_params(parser)
    for arg in parser.args:
        if arg.name in params:
            if isinstance(arg.default, bool):
                # Properly convert Python boolean argument defaults to their string representation
                params[arg.name]['default'] = _bool_to_str(arg.default)
            elif eu.is_enum_type(arg.type):
                params[arg.name][CustomSwaggerAttribute.ENUM_TYPE] = ah.enum_id(arg.type)
                # Only include the enum choices in the Swagger param if there are values,
                # we want the documentation to show a string input box otherwise.
                if arg.metadata.get(api.DocumentationMetadata.ENUM_CHOICES):
                    # Replace the enum choices with those defined on the argument
                    params[arg.name]['enum'] = arg.metadata[api.DocumentationMetadata.ENUM_CHOICES]

        if arg.metadata.get(api.DocumentationMetadata.DEPRECATED):
            params[arg.name][CustomSwaggerAttribute.DEPRECATED] = True

        if arg.metadata.get(api.DocumentationMetadata.HAS_HTML):
            params[arg.name][CustomSwaggerAttribute.HAS_HTML] = True
        elif arg.metadata.get(api.DocumentationMetadata.HAS_JSON):
            params[arg.name][CustomSwaggerAttribute.HAS_JSON] = True
    return params


# Add Swagger property support for deprecated and Enum fields
def field_to_property(field):
    prop = swagger.__field_to_property(field)
    if hasattr(field, '__apidoc__'):
        deprecated = field.__apidoc__.get(api.DocumentationMetadata.DEPRECATED)
        has_html = field.__apidoc__.get(api.DocumentationMetadata.HAS_HTML)
        enum_cls = field.__apidoc__.get(api.DocumentationMetadata.ENUM_CLS)

        if deprecated:
            prop[CustomSwaggerAttribute.DEPRECATED] = True

        if has_html:
            prop[CustomSwaggerAttribute.HAS_HTML] = True

        if enum_cls:
            prop[CustomSwaggerAttribute.ENUM_TYPE] = ah.enum_id(enum_cls)

    return prop


# Monkeypatch
swagger.parser_to_params = parser_to_params
swagger.field_to_property = field_to_property


class Swagger(BaseSwagger):
    def as_dict(self):
        basepath = self.api.base_path
        if len(basepath) > 1 and basepath.endswith('/'):
            basepath = basepath[:-1]
        infos = {
            'title': self.api.title,
            'version': self.api.version,
        }
        if self.api.description:
            infos['description'] = self.api.description
        if self.api.terms_url:
            infos['termsOfService'] = self.api.terms_url
        if self.api.contact and (self.api.contact_email or self.api.contact_url):
            infos['contact'] = {
                'name': self.api.contact,
                'email': self.api.contact_email,
                'url': self.api.contact_url,
            }
        if self.api.license:
            infos['license'] = {'name': self.api.license}
            if self.api.license_url:
                infos['license']['url'] = self.api.license_url

        paths = {}
        tags = []
        for ns in self.api.namespace_registry.values():
            tags.append({
                'name': ns.name,
                'description': ns.description
            })
            for resource, urls, kwargs in ns.resources:
                for url in urls:
                    # Formerly, when building the `paths` collection, this code would only keep the last serialized
                    # resource for a given normalized URL. Now it'll correctly maintain one per URL per request method.
                    norm_path = extract_path(url)
                    serialized_resource = self.serialize_resource(ns, resource, url)
                    paths.setdefault(norm_path, {}).update(serialized_resource)

        specs = {
            'swagger': '2.0',
            'basePath': basepath,
            'paths': not_none(paths),
            'info': infos,
            'produces': list(self.api.representations.keys()),
            'consumes': ['application/json'],
            'securityDefinitions': self.api.authorizations or None,
            'security': self.security_requirements(self.api.security) or None,
            'tags': tags,
            'definitions': self.serialize_definitions() or None,
        }
        return not_none(specs)

    def serialize_definitions(self):
        # By default, only the model definitions that are in-use by one or more endpoints will appear in swagger.
        # However, we want all schema models to be registered, especially the "no view" variants,
        # so that the admin application can leverage them.
        return dict((name, self.serialize_model(name, model)) for name, model in self.api.models.iteritems())

    def register_model(self, model):
        if model not in self.api.models:
            raise ValueError('Model {0} not registered'.format(model))
        specs = self.api.models[model]
        self._registered_models[model] = specs
        if isinstance(specs, dict):
            for name, field in specs.items():
                model_name = None

                if isinstance(field, fields.Nested) and hasattr(field.nested, '__apidoc__'):
                    model_name = field.nested.__apidoc__.get('name')
                elif isinstance(field, fields.List) and hasattr(field.container, '__apidoc__'):
                    model_name = field.container.__apidoc__.get('name')
                elif ((isinstance(field, fields.Raw) or (isclass(field) and issubclass(field, fields.Raw))) and
                      hasattr(field, '__apidoc__') and not field.__apidoc__.get('type')):
                    model_name = field.__apidoc__.get('name')

                # Self-referential schemas will cause recursive stack overflow if we don't check
                # if the nested model was already registered.
                if model_name and model_name not in self._registered_models:
                    self.register_model(model_name)

    def get_actions(self, resource):
        actions = []

        for key in dir(resource.Action):
            action = getattr(resource.Action, key)
            if isinstance(action, str) and hasattr(resource, action):
                actions.append(action)

        return actions

    def serialize_resource(self, ns, resource, url):
        doc = self.extract_resource_doc(resource, url)
        if doc is False:
            return
        operations = {}
        for action in self.get_actions(resource):
            if action not in doc or doc[action] is False:
                continue

            for r in ns.resources:
                if r[2]['endpoint'].endswith('|{}'.format(action)) and r[1][0] == url:
                    break
            else:
                continue

            method = resource.Action.http_method_for_action(action)
            operations[method] = self.serialize_operation(doc, action)
            operations[method]['tags'] = [ns.name]
        return operations

    def extract_resource_doc(self, resource, url):
        doc = getattr(resource, '__apidoc__', {})
        if doc is False:
            return False
        doc['name'] = resource.__name__
        doc['params'] = extract_path_params(url)
        for action in self.get_actions(resource):
            action_doc = doc.get(action, {})
            action_impl = getattr(resource, action)
            if hasattr(action_impl, 'im_func'):
                action_impl = action_impl.im_func
            elif hasattr(action_impl, '__func__'):
                action_impl = action_impl.__func__
            action_doc = merge(action_doc, getattr(action_impl, '__apidoc__', {}))
            if action_doc is not False:
                action_doc['docstring'] = getattr(action_impl, '__doc__')
                action_doc['params'] = self.merge_params({}, action_doc)
            doc[action] = action_doc
        return doc

    def parameters_for(self, doc, method):
        params = super(Swagger, self).parameters_for(doc, method)
        # Parameters are sorted alphabetically by name; the required ones precede the optional ones.
        return sorted(params, key=lambda x: (not x.get('required'), x.get('name')))

    def serialize_operation(self, doc, method):
        operation = super(Swagger, self).serialize_operation(doc, method)
        operation_doc = doc[method]

        # Denote operations as cached for a specific region
        if api.DocumentationMetadata.CACHE_REGION in operation_doc:
            cache_region_name = operation_doc[api.DocumentationMetadata.CACHE_REGION]
            cache_region = cache.dogpile_cache.get_region(cache_region_name)
            operation[CustomSwaggerAttribute.CACHE_REGION] = cache_region_name
            operation[CustomSwaggerAttribute.CACHE_REGION_EXPIRATION] = cache_region.expiration_time

        # Denote operations as deprecated and include our custom, vendor-specific deprecation details
        if api.DocumentationMetadata.DEPRECATED in operation_doc:
            if operation_doc[api.DocumentationMetadata.DEPRECATED]:
                operation['deprecated'] = operation_doc[api.DocumentationMetadata.DEPRECATED]

                if api.DocumentationMetadata.DEPRECATED_ON_DATE in operation_doc:
                    operation[CustomSwaggerAttribute.DEPRECATED_ON_DATE] = ju.isoformat(
                        operation_doc[api.DocumentationMetadata.DEPRECATED_ON_DATE])

                if api.DocumentationMetadata.DEPRECATED_REMOVAL_DATE in operation_doc:
                    operation[CustomSwaggerAttribute.DEPRECATED_REMOVAL_DATE] = ju.isoformat(
                        operation_doc[api.DocumentationMetadata.DEPRECATED_REMOVAL_DATE])

                if api.DocumentationMetadata.DEPRECATED_REASON in operation_doc:
                    operation[CustomSwaggerAttribute.DEPRECATED_REASON] = operation_doc[
                        api.DocumentationMetadata.DEPRECATED_REASON]

        # Include our custom permission information
        if api.DocumentationMetadata.PERMISSIONS in operation_doc:
            operation[CustomSwaggerAttribute.PERMISSIONS] = operation_doc[api.DocumentationMetadata.PERMISSIONS]

        return operation


def _bool_to_str(value):
    return str(bool(value)).lower()


def doc_param(name, description, required=None, min=None, max=None):
    """Create a Swagger-compliant dict that documents the requirements of an API input parameter."""
    doc = dict(description=description)
    if required is not None:
        doc['required'] = _bool_to_str(required)
    if min is not None:
        doc['min'] = min
    if max is not None:
        doc['max'] = max
    return {name: doc}


def handle_api_doc(f, doc):
    if doc is False:
        f.__apidoc__ = False
        return
    unshortcut_params_description(doc)
    for key in 'get', 'post', 'put', 'delete', 'options', 'head', 'patch':
        if key in doc:
            if doc[key] is False:
                continue
            unshortcut_params_description(doc[key])
    f.__apidoc__ = merge(getattr(f, '__apidoc__', {}), doc)
