from flask import current_app

from ct_core_api.api.core.namespace import APINamespace
from ct_core_api.api.core.resource import APIResource

api = APINamespace('config', description="Application Configuration")


@api.route('/')
class AppConfigResource(APIResource):
    def get(self):
        """Get the current application's config.
        The values shown are the canonical string representations of the Python objects.
        This ensures that they can be JSON encoded.
        """
        return {k: repr(v) for k, v in current_app.config.iteritems()}
