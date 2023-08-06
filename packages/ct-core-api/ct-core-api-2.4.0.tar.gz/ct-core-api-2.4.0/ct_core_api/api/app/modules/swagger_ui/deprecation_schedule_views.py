import logging
from datetime import datetime, timedelta

from flask import render_template
from flask.views import View

from ct_core_api.api.core.swagger import doc_utils as du
from ct_core_api.common import datetime_utils as dtu

_logger = logging.getLogger(__name__)


class DeprecationScheduleView(View):
    DEFAULT_DEPRECATION_SCHEDULE_TEMPLATE = 'swagger-ui/deprecated.html'

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
