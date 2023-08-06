from datetime import timedelta

import simplejson as json
from marshmallow import utils as ma_utils


def isoformat(dt, localtime=False, *args, **kwargs):
    """ISO8601-formatted UTC representation of a datetime object.
    The timezone offset portion of the string will be replaced with a "Z" if the UTC offset is 0.
    """
    value = ma_utils.isoformat(dt, localtime=localtime, *args, **kwargs)
    if value.endswith('+00:00'):
        return "{}Z".format(value[:-6])
    return value


def from_iso(datestring):
    """Parse an ISO8601-formatted string into a datetime object.
    The `tzinfo` will be set to None if the UTC offset is 0.
    """
    dt = ma_utils.from_iso(datestring, use_dateutil=True)
    if dt.tzinfo and dt.tzinfo.utcoffset(dt) == timedelta(0):
        return dt.replace(tzinfo=None)
    return dt


def loads(value, **kwargs):
    kwargs.setdefault('use_decimal', True)
    return json.loads(value, **kwargs)


def dumps(value, **kwargs):
    kwargs.setdefault('use_decimal', True)
    return json.dumps(value, **kwargs)
