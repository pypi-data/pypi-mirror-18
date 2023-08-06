import logging
import time
import warnings

from sqlalchemy import exc as sa_exc

__version__ = '2.5.0'


########################################
# Logging
########################################

def _setup_logging():
    logging.basicConfig()
    logging.addLevelName(logging.DEBUG, 'DBG')
    logging.addLevelName(logging.INFO, 'INF')
    logging.addLevelName(logging.WARNING, 'WRN')
    logging.addLevelName(logging.ERROR, 'ERR')
    logging.addLevelName(logging.CRITICAL, 'CRT')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    class DefaultLogFormatter(logging.Formatter):
        """Default log formatter that formats times using UTC (GMT)."""
        FORMAT = "\n[%(asctime)s][%(levelname)s][%(pathname)s:%(lineno)d]\n%(message)s"
        DATE_FORMAT = "%Y-%m-%d %H:%M:%S %Z%z"
        converter = time.gmtime

        def __init__(self, fmt=FORMAT, datefmt=DATE_FORMAT):
            super(DefaultLogFormatter, self).__init__(fmt, datefmt)

    try:
        import colorlog
    except ImportError:
        formatter = DefaultLogFormatter()
    else:
        class DefaultColoredLogFormatter(colorlog.ColoredFormatter):
            DATE_FORMAT = "%Y-%m-%d %H:%M:%S %Z%z"
            converter = time.gmtime

            def __init__(self, *args, **kwargs):
                super(DefaultColoredLogFormatter, self).__init__(*args, datefmt=self.DATE_FORMAT, **kwargs)

        formatter = DefaultColoredLogFormatter((
            '\n%(asctime)s '
            '[%(log_color)s%(levelname)s%(reset)s] '
            '[%(cyan)s%(name)s%(reset)s] '
            '[%(pathname)s:%(lineno)d]\n'
            '%(message_log_color)s%(message)s%(reset)s'),
            reset=True,
            log_colors={
                'DBG': 'bold_cyan',
                'INF': 'bold_green',
                'WRN': 'bold_yellow',
                'ERR': 'bold_red',
                'CRT': 'bold_red,bg_white'},
            secondary_log_colors={
                'message': {
                    'DBG': 'white',
                    'INF': 'bold_white',
                    'WRN': 'bold_yellow',
                    'ERR': 'bold_red',
                    'CRT': 'bold_red'}},
            style='%')

    for handler in logger.handlers:
        if isinstance(handler, logging.StreamHandler):
            break
    else:
        handler = logging.StreamHandler()
        logger.addHandler(handler)
    handler.setFormatter(formatter)


_setup_logging()


########################################
# Warning Filters
########################################
# It is necessary to configure warning filters in the root module because this
# code runs first, regardless of entry point.
# Please refer to ticket #6467 for details on which warnings are being
# suppressed and discussion around how to resolve them.

# SAWarning: Unmanaged access of declarative attribute XXX from non-mapped
# class XXX (desc.fget.__name__, cls.__name__))
warnings.filterwarnings('ignore', category=sa_exc.SAWarning, module='sqlalchemy.ext.declarative.api')
