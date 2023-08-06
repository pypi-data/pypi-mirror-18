"""
API Application
"""
from functools import wraps

from flask import Flask
from werkzeug.utils import cached_property

from ct_core_api.common import string_utils


########################################
# API Application
########################################

class App(Flask):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, instance_relative_config=True, **kwargs)

        # Configure URL handling
        self.url_map.strict_slashes = False  # Ignore differences in the trailing slash

        # Prevent teardown functions from raising
        @self.before_first_request
        def wrap_teardown_funcs():
            self.__wrap_teardown_funcs()

    def register_extension(self, extension, extension_name=None):
        """Register an extension by name to this application.
        Note: This does not handle the initialization of the extension.
        """
        extension_name = extension_name or string_utils.camel_to_snake(extension.__class__.__name__)
        self.extensions = getattr(self, 'extensions', {})
        self.extensions[extension_name] = extension

    def __wrap_teardown_funcs(self):
        """Prevent Flask teardown functions from raising.
        Extensions can register their own and they may not have appropriate exception handling in place.
        """
        def wrap_teardown_func(teardown_func):
            @wraps(teardown_func)
            def log_teardown_error(*args, **kwargs):
                try:
                    teardown_func(*args, **kwargs)
                except Exception as exc:
                    self.logger.exception(exc)
            return log_teardown_error

        if self.teardown_request_funcs:
            for bp, func_list in self.teardown_request_funcs.items():
                for i, func in enumerate(func_list):
                    self.teardown_request_funcs[bp][i] = wrap_teardown_func(func)

        if self.teardown_appcontext_funcs:
            for i, func in enumerate(self.teardown_appcontext_funcs):
                self.teardown_appcontext_funcs[i] = wrap_teardown_func(func)


class APIApp(App):
    @cached_property
    def api_extensions(self):
        from flask_restplus.api import Api
        return {name: ext for name, ext in self.extensions.iteritems() if isinstance(ext, Api)}

    def is_api_request(self):
        # TODO: Further testing is required to determine if this meets all usecases
        return any(x._has_fr_route() for x in self.api_extensions.values())
