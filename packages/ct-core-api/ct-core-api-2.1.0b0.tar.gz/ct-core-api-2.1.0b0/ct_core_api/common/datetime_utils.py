from datetime import datetime

from pytz import timezone, UTC


class Zone(object):
    UTC = UTC.zone
    US_EASTERN = 'US/Eastern'
    US_CENTRAL = 'US/Central'
    US_MOUNTAIN = 'US/Mountain'
    US_PACIFIC = 'US/Pacific'


class TimeZone(object):
    UTC = UTC
    EASTERN = timezone(Zone.US_EASTERN)
    CENTRAL = timezone(Zone.US_CENTRAL)
    MOUNTAIN = timezone(Zone.US_MOUNTAIN)
    PACIFIC = timezone(Zone.US_PACIFIC)


def combine_date_time(d, t):
    """Return datetime having these date and time components."""
    return datetime.combine(d, t)


def make_datetime(dt):
    """Return a datetime from a tuple of (date, time) or pass through."""
    return combine_date_time(*dt) if isinstance(dt, tuple) else dt


def make_naive_datetime(dt):
    """Convert local datetime to naive datetime. Return an offset unaware datetime (ie. no tz info)."""
    dt = make_datetime(dt)
    return dt.replace(tzinfo=None)


def make_timezone(tz):
    """Return a pytz timezone from a timezone string or pass through."""
    return timezone(tz) if isinstance(tz, (str, unicode)) else tz


def localize_datetime(dt, tz):
    """Convert datetime to local datetime in this timezone."""
    dt = make_datetime(dt)
    tz = make_timezone(tz)
    return tz.localize(make_naive_datetime(dt))


def utc_to_local_datetime(dt, tz):
    """Convert UTC datetime to local datetime in this timezone."""
    dt = make_datetime(dt)
    tz = make_timezone(tz)
    return dt.replace(tzinfo=TimeZone.UTC).astimezone(tz)


def local_to_utc_datetime(dt, tz):
    """Convert local datetime in this timezone to UTC datetime.
    Return an offset unaware datetime (ie. no tz info).
    """
    dt = make_datetime(dt)
    tz = make_timezone(tz)
    return make_naive_datetime(localize_datetime(dt, tz).astimezone(TimeZone.UTC))


def local_dt_str_to_utc_datetime(dt_str, tz):
    """Convert a datetime string with a timezone into a UTC datetime.
    If a tuple/list of (date, time) strings are passed, join them and convert.
    """
    dt_str = ' '.join(list(dt_str)) if isinstance(dt_str, (tuple, list)) else dt_str
    dt = datetime.strptime(dt_str, '%m/%d/%Y %H:%M')
    return local_to_utc_datetime(dt, tz)


def local_d_str_to_utc_datetime(d_str, tz):
    """Convert a date string with a timezone into a UTC datetime."""
    dt = datetime.strptime(d_str, '%m/%d/%Y')
    return local_to_utc_datetime(dt, tz)


def utc_to_et(dt):
    """Convert UTC datetime to Eastern datetime."""
    dt = make_datetime(dt)
    return utc_to_local_datetime(dt, TimeZone.EASTERN)


def format_datetime(dt, format="%Y-%m-%d %H:%M:%S %Z%z", tz=None):
    """Format the datetime using the given format string.
    If a timezone is provided, the time will be localized from UTC.
    """
    if dt is not None:
        dt = make_datetime(dt)
        if tz is not None:
            dt = utc_to_local_datetime(dt, tz)
        dt = dt.strftime(format).strip()
    return dt


def format_datetime_et(dt, format="%m/%d/%Y %H:%M %Z"):
    return format_datetime(dt, format=format, tz=TimeZone.EASTERN)
