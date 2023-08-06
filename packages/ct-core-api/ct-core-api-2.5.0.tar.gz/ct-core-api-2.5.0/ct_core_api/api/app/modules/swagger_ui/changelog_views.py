import logging

import yaml
from flask import render_template
from flask.views import View

from ct_core_api.api.core import response

_logger = logging.getLogger(__name__)


class ChangelogView(View):
    DEFAULT_CHANGELOG_TEMPLATE = 'swagger-ui/changelog.html'

    def __init__(self, changelog_yml_file, template_name=None):
        self.changelog_yml_file = changelog_yml_file
        self.template_name = template_name or self.DEFAULT_CHANGELOG_TEMPLATE

    def dispatch_request(self):
        try:
            with open(self.changelog_yml_file, 'rt') as f:
                changelog = yaml.load_all(f.read())
        except IOError as exc:
            _logger.warn("Unable to load changelog: {}".format(exc))
            response.abort(404)
        return render_template(self.template_name, changelog=changelog)
