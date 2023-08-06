from __future__ import absolute_import

import logging

from flask import has_request_context, request, g, got_request_exception

from ct_core_api.api.common import api_helpers as ah, log_utils as lu


########################################
# Configure Logging
########################################

def init_app(app):
    # Gather the logging configuration
    default_log_level = logging.DEBUG if app.debug or app.testing else logging.INFO
    config_log_level = app.config.get('LOG_LEVEL')

    log_level = config_log_level if config_log_level is not None else default_log_level
    log_msg_format = app.config.get('LOG_MSG_FORMAT')
    log_date_format = app.config.get('LOG_DATE_FORMAT')
    log_file_path = app.config.get('LOG_FILE_PATH')

    # Gather the loggers we care about
    sqla_logger = logging.getLogger('sqlalchemy')
    sqla_pool_logger = logging.getLogger('sqlalchemy.pool')
    ct_core_api_logger = logging.getLogger('ct_core_api')
    loggers = [app.logger, sqla_logger, sqla_pool_logger, ct_core_api_logger]
    handlers = []

    # Remove the app logger's handlers
    for handler in app.logger.handlers:
        app.logger.removeHandler(handler)

    # Set the log level for the app logger
    app.logger.setLevel(log_level)

    # Setup the rotating file handler (optional)
    if not app.testing and log_file_path:
        # Rotating file handler
        file_handler = logging.handlers.RotatingFileHandler(
            log_file_path, mode='a', maxBytes=1 * 1024 * 1024, backupCount=10)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter(log_msg_format, datefmt=log_date_format))
        handlers.append(file_handler)

    # Add handlers to loggers
    for logger in loggers:
        for handler in handlers:
            logger.addHandler(handler)

    # Configure connection pool debug logging
    if app.config.get('POOL_DEBUG_LOGGING'):
        sqla_pool_logger.setLevel(logging.DEBUG)

    # Include this extra information in all log messages (functions get executed at log time)
    if app.config.get('LOG_VERBOSE_DEV_MESSAGES', False):
        extra_info = lu.ExtraInfo()
        extra_info['ip'] = _ip_extra_info
        extra_info['uid'] = _uid_extra_info
        extra_info['ua'] = _ua_extra_info
        extra_info['url'] = _url_extra_info

        app._logger = lu.ExtraInfoLogger(app.logger, extra_info)

    # Connect the exception logging functions to the `got_request_exception` signal
    got_request_exception.connect(lu.log_api_exception, app)
    got_request_exception.connect(lu.log_api_exception_to_browser_console, app)


def _uid_extra_info():
    return str(g.user.id).upper() if hasattr(g, 'user') and hasattr(g.user, 'id') and g.user.id is not None else None


def _ip_extra_info():
    return has_request_context() and ah.get_remote_addr() or None


def _ua_extra_info():
    return has_request_context() and ah.get_user_agent_summary() or None


def _url_extra_info():
    return has_request_context() and request.url or None
