
import os
import pytz
import re

from datetime import datetime
from functools import wraps
from .settings import AGILE_API_SETTINGS as SETTINGS


def datestring_to_ms_datestring(datetime_string):
    """Converts datetime string in ISO format `2016-11-22T20:46:57-08:00Z` to MS date string ( Json.NET < 4.5 )
        
    """
    datetime_string = "{0}{1}".format(*datetime_string.rsplit(':', 1))
    if '+' in datetime_string:
        date, offset = datetime_string.split('+')
        offset = "+{0}".format(offset[:-1])
    else:
        date, offset = datetime_string.rsplit('-', 1)
        offset = "-{0}".format(offset[:-1])
    date_obj = datetime.strptime(date,'%Y-%m-%dT%H:%M:%S')
    epoch = int(date_obj.timestamp() * 1000)
    ms_datestring = "/Date({0}{1})/".format(epoch, offset)
    return ms_datestring


def ms_datestring_to_datetime(datetime_string):
    """Converts MS date string ( Json.NET < 4.5 ) in the format '/Date(1451953800000-0600)/' to a python date object 

    """
    DATETIME_REGEX = r'([0-9\+\-]+)'
    datetime_string = re.search(DATETIME_REGEX, datetime_string).groups()[0]
    epoch = abs(int(datetime_string[:-5]))
    offset = int(datetime_string[-5:]) / 100
    seconds = epoch / 1000
    offset_seconds = offset * 3600
    unaware_dt = datetime.utcfromtimestamp(seconds + offset_seconds)
    local_tz = pytz.timezone(SETTINGS['AGILE_TIMEZONE'])
    aware_dt = local_tz.localize(unaware_dt)
    return aware_dt


def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy.

    """
    z = x.copy()
    z.update(y)
    return z


def method_name(func):
    """Method wrapper that adds the name of the method being called to its arguments list in Pascal case

    """
    @wraps(func)
    def _method_name(*args, **kwargs):
        name = to_pascal_case(func.__name__)
        return func(name=name, *args, **kwargs)
    return _method_name


def strftime_agile(date):
    """Convenience date format function
    
    """
    return date.strftime(SETTINGS['AGILE_DATE_FORMAT'])


def to_camel_case(s):
    """Transform underscore separated string to camel case

    """
    s = to_pascal_case(s)
    return s[0].lower() + s[1:]


def to_pascal_case(s):
    """Transform underscore separated string to pascal case

    """
    return re.sub(r'(?!^)_([a-zA-Z])', lambda m: m.group(1).upper(), s.capitalize())


def to_underscore(s):
    """Transform camel or pascal case to underscore separated string

    """
    return re.sub(
            r'(?!^)([A-Z]+)',
            lambda m: "_{0}".format(m.group(1).lower()),
            re.sub(r'(?!^)([A-Z]{1}[a-z]{1})', lambda m: "_{0}".format(m.group(1).lower()), s)
        ).lower()

