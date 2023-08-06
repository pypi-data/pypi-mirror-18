import logging
import traceback
import sys
from collections import OrderedDict

from flask import has_request_context, request, g
from texttable import Texttable
from werkzeug._compat import iteritems

from ct_core_api.common import string_utils as su


########################################
# Extra Info Logger
########################################

class ExtraInfo(OrderedDict):
    """Container class for extra logging information.
    Maintains insertion order so that the logger can output consistent messages.
    If a key references a function it will be called and its value returned.
    """
    def __getitem__(self, key):
        value = super(ExtraInfo, self).__getitem__(key)
        if hasattr(value, '__call__'):
            return value()
        return value


class ExtraInfoLogger(logging.LoggerAdapter):
    def __init__(self, logger, extra):
        super(ExtraInfoLogger, self).__init__(logger, extra)

    @property
    def name(self):
        return self.logger.name

    def process(self, msg, kwargs):
        msg_fmt = "[{}]\n{}"
        try:
            extra_info = ' | '.join(["{}: {}".format(k, v) for k, v in self.extra.items() if v is not None])
            if extra_info:
                msg = msg_fmt.format(extra_info, msg)
        except Exception as exc:
            # Handle logging exceptions to prevent application errors
            msg = msg_fmt.format("{} Exception: {}".format(self.__class__.__name__, exc), msg)
        return msg, kwargs


########################################
# API Exception Logging
########################################

def gather_api_exception_log_data(exclude_headers={'Cookie', 'User-Agent'}):
    request_info = []
    browser_info = []
    user_info = []

    if has_request_context():
        if request.path:
            request_info.append(('Path', request.path))
        if request.query_string:
            request_info.append(('Query String', request.query_string))
        if request.method:
            request_info.append(('Method', request.method))
        if request.remote_addr:
            request_info.append(('IP', request.remote_addr))
        if request.values:
            request_info.append((
                'Params',
                '\n'.join([repr(x) for x in list(
                    iteritems(su.strip_sensitive_data_from_multidict(request.values), multi=True))])))
        if request.headers:
            headers = '\n'.join(
                sorted(["{}: {}".format(k, v) for k, v in list(request.headers) if k not in exclude_headers]))
            request_info.append(("Headers\n----------\nExcludes:\n{}".format(',\n'.join(exclude_headers)), headers))

        if request.user_agent.string:
            browser_info.append(('User Agent', request.user_agent.string))
        if request.user_agent.platform:
            browser_info.append(('Platform', request.user_agent.platform))
        if request.user_agent.browser:
            browser_info.append(('Browser', request.user_agent.browser))
        if request.user_agent.version:
            browser_info.append(('Browser Version', request.user_agent.version))

    if g:
        if hasattr(g, 'user') and g.user:
            if g.user.id is not None:
                user_info.append(('Id', g.user.id))
            if g.user.email:
                user_info.append(('Email', g.user.email))
            if g.user.full_name:
                user_info.append(('Name', g.user.full_name))

    return request_info, browser_info, user_info


def log_api_exception(sender, exception, **extra):
    fallback_message = u'Exception raised inside `log_api_exception`!'
    try:
        messages = []

        # If debugging or testing, log verbose request, browser, and user information
        if (sender.debug or sender.testing) and sender.config.get('API_LOG_EXTRA_REQUEST_INFO_ON_REQUEST_EXCEPTION'):
            request_info, browser_info, user_info = gather_api_exception_log_data()

            if request_info:
                table = Texttable()
                table.set_cols_width([10, 62])  # Accommodates an overall table width of 79 characters
                table.add_rows([('Request', 'Information')] + request_info)
                messages.append(table.draw())

            if browser_info:
                table = Texttable()
                table.add_rows([('Browser', 'Information')] + browser_info)
                messages.append(table.draw())

            if user_info:
                table = Texttable()
                table.add_rows([('User', 'Information')] + user_info)
                messages.append(table.draw())
        else:
            messages.append(u'{0}'.format(exception))

        message = '\n\n'.join(messages) if messages else None
    except Exception:
        message = fallback_message
    sender.logger.exception(message, **extra)


########################################
# API Browser Console Logging
########################################

# https://github.com/ccampbell/chromelogger-python
# Required Chrome extension: https://chrome.google.com/extensions/detail/noaneddfkdjfnfdakjjmocngnfkfehhd

def log_api_warning_message_to_browser_console(message):
    """Log an API warning message to the browser's console."""
    try:
        import chromelogger
        chromelogger.warn('%cAPI Server Warning:', 'color: DarkOrange; font-weight: bold', message)
    except Exception:
        pass  # Failures here should not prevent the API error response


def log_api_exception_to_browser_console(sender, exception, **extra):
    """Log an API exception to the browser's console."""
    if sender.debug and sender.config.get('API_LOG_EXCEPTIONS_TO_BROWSER_CONSOLE'):
        try:
            import chromelogger

            type_, value_, traceback_ = sys.exc_info()
            tbs = traceback.extract_tb(traceback_)
            exc_only = traceback.format_exception_only(type_, value_)

            group_func = chromelogger.group_collapsed
            chromelogger.group_collapsed("%cAPI Server Error:", 'color: red;', str(exc_only[-1]))
            chromelogger.log('Traceback (most recent call last):')
            for i, tb in enumerate(tbs):
                if i == len(tbs) - 1:
                    group_func = chromelogger.group  # Expand the last stack frame
                group_func('%cFile "%s", line %i, in %s', 'font-weight: normal;', tb[0], tb[1], tb[2])
                chromelogger.log(tb[3])
                chromelogger.group_end()
            chromelogger.warn(''.join(exc_only))
            chromelogger.group_end()
        except Exception:
            pass  # Failures here should not prevent the API error response
