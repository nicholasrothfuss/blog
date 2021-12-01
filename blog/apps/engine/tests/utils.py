"""Provides various utilities for testing the blog engine application."""
import datetime
from django.utils import timezone
from pytest_django.asserts import assertContains, assertNotContains


ONE_DAY_AGO = timezone.now() - datetime.timedelta(days=1)


#-- Assertions for testing page content --#

def assert_contains_post_title(response, text, header_tag='h2'):
    expected_str = f'<{header_tag}>{text}</{header_tag}>'
    assertContains(response, expected_str)


def assert_contains_post_permalinks(response, expected_url):
    expected_str = f'<a href="{expected_url}">Permalink</a>'
    assertContains(response, expected_str)


def assert_not_contains_post_categories(response):
    assertNotContains(response, 'Posted in')


#-- Other custom assertions --#

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