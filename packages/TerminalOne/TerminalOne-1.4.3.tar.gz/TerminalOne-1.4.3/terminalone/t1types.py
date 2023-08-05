# -*- coding: utf-8 -*-
"""Provides field type conversion functions T1 data classes."""

from datetime import datetime
from terminalone.utils import FixedOffset


def int_to_bool(value):
    """Convert integer string {"0","1"} to its corresponding bool"""
    try:
        return bool(int(value))
    except ValueError:
        raise TypeError('must supply integer string')


def none_to_empty(val):
    """Convert None to empty string.

    Necessary for fields that are required POST but have no logical value.
    """
    if val is None:
        return ""
    return val


def enum(all_vars, default):
    """Check input against accepted set or return a default."""

    def get_value(test_value):
        if test_value in all_vars:
            return test_value
        else:
            return default

    return get_value


def default_empty(default):
    """Check an input against its falsy value or return a default."""

    def get_value(test_value):
        if test_value:
            return test_value
        else:
            return default

    return get_value


def strpt(dt_string):
    """Convert ISO string time to datetime.datetime. No-op on datetimes"""
    if isinstance(dt_string, datetime):
        return dt_string
    if dt_string[-5] == '-' or dt_string[-5] == '+':
        offset_str = dt_string[-5:]
        dt_string = dt_string[:-5]
        offset = int(offset_str[-4:-2]) * 60 + int(offset_str[-2:])
        if offset_str[0] == "-":
            offset = -offset
    else:
        offset = 0

    return datetime.strptime(dt_string, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=FixedOffset(offset))


def strft(dt_obj, null_on_none=False):
    """Convert datetime.datetime to ISO string.

    :param null_on_none: bool Occasionally, we will actually want to send an
        empty string where a datetime would typically go. For instance, if a
        strategy has an end_date set, but then wants to change to use
        campaign end date, the POST will normally omit the end_date field
        (because you cannot send it with use_campaign_end).
        However, this will cause an error because there was an end_date set
        previously. So, we need to send an empty string to indicate that it
        should be nulled out. In cases like this, null_on_none should be set
        to True in the entity's _push dict using a partial to make it a
        single-argument function. See strategy.py
    :raise AttributeError: if not provided a datetime
    :return: str
    """
    try:
        return dt_obj.strftime("%Y-%m-%dT%H:%M:%S")
    except AttributeError:
        if dt_obj is None and null_on_none:
            return ""
        raise
