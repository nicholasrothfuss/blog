"""Provides various utilities for testing the blog engine application."""
import datetime
from django.utils import timezone


ONE_DAY_AGO = timezone.now() - datetime.timedelta(days=1)


def assert_is_now(dt):
    assert 0 <= (timezone.now() - dt).seconds < 1


def tz_datetime(year, month, day, hour=0, minute=0, second=0):
    """
    Creates a datetime.datetime instance with the specified parameters and a 
    tzinfo field set to the Django-defined current time zone.
    """
    return datetime.datetime(
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        second=second,
        tzinfo=timezone.get_current_timezone()
    )