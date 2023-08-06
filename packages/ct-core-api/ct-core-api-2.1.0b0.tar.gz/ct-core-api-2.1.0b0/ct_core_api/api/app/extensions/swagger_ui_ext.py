from __future__ import absolute_import

import logging
import os
from datetime import datetime, timedelta

import yaml
from flask import Blueprint, make_response, redirect, render_template, url_for
from flask.views import View

from ct_core_api.api import core
from ct_core_api.api.core import response
from ct_core_api.api.core.swagger import doc_utils as du
from ct_core_api.common import datetime_utils as dtu

_logger = logging.getLogger(__name__)


########################################
# Configure Swagger UI
########################################

def init_app(app):
    # Register Swagger UI blueprint
    app.register_blueprint(swagger_ui_bp)

    # Register cached swagger.json route
    @app.route('/cached/swagger.json')
    def cached_specs():
        return redirect(url_for('cacheable_specs', cache_version=app.config.get('GIT_REVISION', '')))

    # Register cache-able swagger.json route
    @app.route('/cached/<cache_version>/swagger.json')
    def cacheable_specs(cache_version):
        if cache_version == app.config.get('GIT_REVISION'):
            return make_response(app.view_functions['specs']())
        response.abort(404)

    # Register enums.json route
    @app.route('/enums.json')
    def enums():
        # FIXME: Figure out how to gather enums
        enum_proxies = []  # eu.get_all_enum_proxies()
        # Only include enums that are explicitly declared as external or enums that are used in the API
        exposed_enum_ids = du.parse_enum_ids(
            app.extensions['restplus-api-v1'].resources,
            app.extensions['restplus-api-v1'].models)

        def is_exposed_enum(enum_data):
            return enum_data['name'] in exposed_enum_ids

        def is_external_enum(enum_data):
            return enum_data['metadata'] and enum_data['metadata'].get('is_external')

        exposed_enum_proxies = filter(lambda x: is_external_enum(x) or is_exposed_enum(x), enum_proxies)

        return core.make_json_response(dict(enums=exposed_enum_proxies), 200)

    # Register "changelog" route
    api_changelog_path = app.config.get('API_CHANGELOG_PATH') or os.path.join(app.root_path, 'changelog.yml')
    app.add_url_rule('/changelog', view_func=ChangelogView.as_view('changelog', api_changelog_path))

    # Register "deprecation schedule" route
    deprecated_endpoint_warning_window = app.config.get('API_DEPRECATED_ENDPOINT_WARNING_WINDOW')
    app.add_url_rule(
        '/deprecated',
        view_func=DeprecationScheduleView.as_view(
            'deprecated', app.extensions['restplus-api-v1'], warning_window=deprecated_endpoint_warning_window))


swagger_ui_bp = Blueprint(
    'swagger-ui',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/swagger')


@swagger_ui_bp.add_app_template_global
def swagger_ui_static(filename):
    return url_for('swagger-ui.static', filename='swagger-ui/{0}'.format(filename))


class ChangelogView(View):
    DEFAULT_CHANGELOG_TEMPLATE = 'api/changelog.html'

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


class DeprecationScheduleView(View):
    DEFAULT_DEPRECATION_SCHEDULE_TEMPLATE = 'api/deprecated.html'

    def __init__(self, api, warning_window=timedelta(weeks=1), template_name=None):
        self.api = api
        self.warning_window = warning_window
        self.template_name = template_name or self.DEFAULT_DEPRECATION_SCHEDULE_TEMPLATE

    def dispatch_request(self):
        now = datetime.utcnow()
        error_window = timedelta(0)

        deprecated_operations = []

        for resource_entry in self.api.resources:
            operation_info = du.parse_api_resource_operation_info(resource_entry)

            if operation_info['is_deprecated']:
                deprecated_removal_date = operation_info['deprecated_removal_date']
                deprecated_on_date = operation_info['deprecated_on_date']
                time_remaining = deprecated_removal_date.date() - now.date()

                deprecated_operations.append((
                    dtu.utc_to_local_datetime(deprecated_removal_date, dtu.TimeZone.EASTERN).strftime('%Y-%m-%d'),
                    dtu.utc_to_local_datetime(deprecated_on_date, dtu.TimeZone.EASTERN).strftime('%Y-%m-%d'),
                    time_remaining,
                    str(time_remaining).rsplit(',', 1)[0],
                    operation_info['resource'],
                    operation_info['endpoint'],
                    operation_info['method'],
                    operation_info['url']))

        return render_template(
            self.template_name,
            deprecated_operations=sorted(deprecated_operations),
            warning_window=self.warning_window,
            error_window=error_window)
