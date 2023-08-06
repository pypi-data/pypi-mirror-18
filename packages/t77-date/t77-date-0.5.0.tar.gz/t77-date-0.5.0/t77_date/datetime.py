"""datetime.datetime and datetime.date related functions"""
from __future__ import absolute_import
from datetime import timedelta, date, datetime


def start_of_day(val):
    """
    Return a new datetime with values that represent a start of a day.
    :param val: Date to ...
    :type val: datetime.datetime | datetime.date
    :rtype: datetime.datetime
    """
    if type(val) == date:
        val = datetime.fromordinal(val.toordinal())
    return val.replace(hour=0, minute=0, second=0, microsecond=0)


def end_of_day(val):
    """
    Return a new datetime with values that represent a end of a day.
    :param val: Date to ...
    :type val: datetime.datetime | datetime.date
    :rtype: datetime.datetime
    """
    if type(val) == date:
        val = datetime.fromordinal(val.toordinal())
    return start_of_day(val) + timedelta(days=1, microseconds=-1)


def start_of_month(val):
    """
    Return a new datetime with values that represent a start of a month.
    :param val: Date to ...
    :type val: datetime.datetime | datetime.date
    :rtype: datetime.datetime
    """
    if type(val) == date:
        val = datetime.fromordinal(val.toordinal())
    return start_of_day(val).replace(day=1)


def end_of_month(val):
    """
    Return a new datetime with values that represent a end of a month.
    :param val: Date to ...
    :type val: datetime.datetime | datetime.date
    :rtype: datetime.datetime
    """
    if type(val) == date:
        val = datetime.fromordinal(val.toordinal())
    if val.month == 12:
        return start_of_month(val).replace(year=val.year + 1, month=1) \
               - timedelta(microseconds=1)
    else:
        return start_of_month(val).replace(month=val.month + 1) \
               - timedelta(microseconds=1)


def _set_week_day(val, week_day, val_weekday, sign):
    if val_weekday == week_day:
        return val

    diff = sign * (val_weekday - week_day)
    diff = -diff if diff < 0 else 7 - diff
    val += sign * timedelta(days=diff)

    return val


def set_next_week_day(val, week_day, iso=False):
    """
    Set week day.
    New date will be greater or equal than input date.
    :param val: datetime or date
    :type val: datetime.datetime | datetime.date
    :param week_day: Week day to set
    :type week_day: int
    :param iso: week_day in ISO format, or not
    :type iso: bool
    :return: datetime.datetime | datetime.date
    """
    return _set_week_day(val, week_day,
                         val.isoweekday() if iso else val.weekday(), sign=1)


def set_prev_week_day(val, week_day, iso=False):
    """
    Set week day.
    New date will be less or equal than input date.
    :param val: datetime or date
    :type val: datetime.datetime | datetime.date
    :param week_day: Week day to set
    :type week_day: int
    :param iso: week_day in ISO format, or not
    :type iso: bool
    :return: datetime.datetime | datetime.date
    """
    return _set_week_day(val, week_day,
                         val.isoweekday() if iso else val.weekday(), sign=-1)
